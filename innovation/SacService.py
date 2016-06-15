import os
from ctypes import cdll, c_int, create_string_buffer, c_char_p, byref, POINTER
import traceback
import threading
import collections
from sacService.gcfparser import PARSE_OK, MESSAGE_CALL, BT_INTEGER, BT_STRING, BT_LIST, GCFStruct, cast, GCFFeatureValue

# Thread class to handle incoming CALL messages after initialization


class MessageHandlerThread (threading.Thread):

    def __init__(self,):
        threading.Thread.__init__(self)
        self.name = "MessageHandlerThread"

    def run(self):
        print "Starting " + self.name
        self._handle_incoming_systemcalls()
        print "Exiting " + self.name


class SacService(MessageHandlerThread):

    def __init__(self, appName, libPath, port=6010):
        super(SacService, self).__init__()
        self.appName = appName  # The name of the application
        self.iSizeReadbuffer = 80000  # Not sure what the max message size is
        os.environ['PATH'] = libPath + ';' + os.environ['PATH']
        self.libSac = cdll.LoadLibrary('sac.dll')
        self.libGcf = cdll.LoadLibrary('parsercreator.dll')
        self.sysCalls = {}  # Must override
        # Hack for the fact that in a recres, the fv needs special handling
        # when serializing. i.e instead of straight values dict entries get
        # stuck into lists and ints become strings
        self.addingFV = False
        self.port = port

    def load(self):
        # Create the parser
        self.gcfParserHandle = c_int()
        gcfParseError = self.libGcf.GCFParse_Init(byref(self.gcfParserHandle))
        if PARSE_OK != gcfParseError:
            print "Not able to init parser"

        # establish connection
        self.hSacConnection = self.libSac.sss_open(
            "127.0.0.1|" + str(self.port), 0)
        if 0 == self.hSacConnection:
            print("Not able to open connection")
            raise Exception("Not able to open connection")
            exit

        # register the client
        pRegMessages = ["CTRL REGS " + self.appName + " GCF_Version='1.0' INFO='" + self.appName + " : Nuance Communications Aachen GmbH ID_Diagnostics=0.1.2' VERSION='V1.00' CONFIG={  };",
                        "CTRL REGA " + self.appName + " ADDR=" + self.appName + ";"]
        for sysCall in self.sysCalls.keys():  # Add all the system calls
            # Add the registration end message
            pRegMessages.append(
                "CTRL REGC " + self.appName + " CALL=" + sysCall + ";")
        # Add the registration end message
        pRegMessages.append("CTRL REGF " + self.appName + ";")

        for msg in pRegMessages:
            iSendedBytes = self.libSac.sss_write(
                self.hSacConnection, msg, len(msg))
            if 0 == iSendedBytes:
                print "Message was not sent"

        # Wait until we get the first message from natp.
        natpInitComplete = 0
        iErrorCodeRead = 1
        iReadBytes = c_int()
        ReadText = create_string_buffer('\000' * self.iSizeReadbuffer)
        while 0 != iErrorCodeRead and 0 == natpInitComplete:
            iErrorCodeRead = self.libSac.sss_read(
                self.hSacConnection, byref(ReadText), self.iSizeReadbuffer, byref(iReadBytes))
            print "Main thread Received following message", ReadText.value
            if "GCFROUTER MODE=" in ReadText.value:
                natpInitComplete = 1

        # And start the handler thread
        self.start()

    def stop(self):
        try:
            # Should terminate the handler thread but I don't know this is
            # safe.
            self.libSac.sss_close(self.hSacConnection)
            self.join()
            # after the join the parser must not be in use.
            self.libGcf.GCFParse_DeInit(byref(self.gcfParserHandle))
        except:
            raise Exception("Unable to disconnect")

    def sendMsg(self, msg):
        iSendedBytes = self.libSac.sss_write(
            self.hSacConnection, msg, len(msg))
        if 0 == iSendedBytes:
            print "Message was not sent"

    def _addList(self, name, values):
        gcfList = POINTER(GCFFeatureValue)()

        stat = self.libGcf.GCFStruct_InitListFV(byref(gcfList), name)
        if PARSE_OK != stat:
            print "Not able create a list"

        for value in values:
            if isinstance(value, str):
                stat = self.libGcf.GCFStruct_AppendStringListFV(gcfList, value)
                if PARSE_OK != stat:
                    print "Not able to add a string to a list"
            elif isinstance(value, unicode):
                # Unicode strings don't seem to work in this case so convert it to a regular string
                # BEWARE there is likely a chance to lose some information
                # here.
                stat = self.libGcf.GCFStruct_AppendStringListFV(
                    gcfList, str(value))
                if PARSE_OK != stat:
                    print "Not able to add a unicode string to a list"
            elif isinstance(value, int):
                stat = self.libGcf.GCFStruct_AppendIntListFV(gcfList, value)
                if PARSE_OK != stat:
                    print "Not able to add a integer to a list"
            if isinstance(value, long):
                stat = self.libGcf.GCFStruct_AppendStringListFV(
                    gcfList, str(value))
                if PARSE_OK != stat:
                    print "Not able to add a string to a list"
            elif isinstance(value, list):
                gcSubfList = self._addList(None, value)
                stat = self.libGcf.GCFStruct_AppendListFV(gcfList, gcSubfList)
                if PARSE_OK != stat:
                    print "Not able to add the list to the list"
            elif isinstance(value, dict):
                gcSubfList = self._addDict(None, value)
                stat = self.libGcf.GCFStruct_AppendListFV(gcfList, gcSubfList)
                if PARSE_OK != stat:
                    print "Not able to add the dict to the list"

        return gcfList

    def _addDict(self, dictName, values):
        gcfList = POINTER(GCFFeatureValue)()

        stat = self.libGcf.GCFStruct_InitListFV(byref(gcfList), dictName)
        if PARSE_OK != stat:
            print "Not able create a list"

        if dictName == 'fv':
            self.addingFV = True

        for name in values.keys():
            if isinstance(values[name], str):
                if self.addingFV:
                    gcfElementList = POINTER(GCFFeatureValue)()
                    stat = self.libGcf.GCFStruct_InitListFV(
                        byref(gcfElementList), name)
                    if PARSE_OK != stat:
                        print "Not able create a list"
                    stat = self.libGcf.GCFStruct_AppendStringListFV(
                        gcfElementList, values[name])
                    if PARSE_OK != stat:
                        print "Not able to add a string to a dict"
                    stat = self.libGcf.GCFStruct_AppendListFV(
                        gcfList, gcfElementList)
                    if PARSE_OK != stat:
                        print "Not able to add the sublist to the list"
                else:
                    stat = self.libGcf.GCFStruct_AppendStringFV2ListFV(
                        gcfList, name, values[name])
                    if PARSE_OK != stat:
                        print "Not able to add a string to a dict"
            elif isinstance(values[name], int) or isinstance(values[name], long):
                if self.addingFV:
                    gcfElementList = POINTER(GCFFeatureValue)()
                    stat = self.libGcf.GCFStruct_InitListFV(
                        byref(gcfElementList), name)
                    if PARSE_OK != stat:
                        print "Not able create a list"
                    stat = self.libGcf.GCFStruct_AppendStringListFV(
                        gcfElementList, str(values[name]))
                    if PARSE_OK != stat:
                        print "Not able to add a string to a dict"
                    stat = self.libGcf.GCFStruct_AppendListFV(
                        gcfList, gcfElementList)
                    if PARSE_OK != stat:
                        print "Not able to add the sublist to the list"
                else:
                    stat = self.libGcf.GCFStruct_AppendIntFV2ListFV(
                        gcfList, name, values[name])
                    if PARSE_OK != stat:
                        print "Not able to add a integer to a dict"
            elif isinstance(values[name], list):
                gcSubfList = self._addList(name, values[name])
                stat = self.libGcf.GCFStruct_AppendListFV(gcfList, gcSubfList)
                if PARSE_OK != stat:
                    print "Not able to add the list to the dict"
            elif isinstance(values[name], dict):
                gcSubfList = self._addDict(name, values[name])
                stat = self.libGcf.GCFStruct_AppendListFV(gcfList, gcSubfList)
                if PARSE_OK != stat:
                    print "Not able to add the dict to the dict"

        if dictName == 'fv':
            self.addingFV = False
        return gcfList

    def sendResponse(self, params, resultName, resultValue):
        # Create the response
        gcfRespHeader = POINTER(GCFStruct)()
        gcfParseError = self.libGcf.GCFStruct_CreateRespHeader(
            self.parsedStruct, byref(gcfRespHeader))
        if PARSE_OK != gcfParseError:
            print "Not able to create the response header"

        gcfParseError = self.libGcf.GCFStruct_AppendIdentFV(
            gcfRespHeader, resultName, resultValue)
        if PARSE_OK != gcfParseError:
            print "Not able to add the result to the response"

        for param in params.keys():
            if isinstance(params[param], str):
                gcfParseError = self.libGcf.GCFStruct_AppendStringFV(
                    gcfRespHeader, param, params[param])
                if PARSE_OK != gcfParseError:
                    print "Not able to add the result to the response"
            elif isinstance(params[param], int) or isinstance(params[param], long):
                gcfParseError = self.libGcf.GCFStruct_AppendIntFV(
                    gcfRespHeader, param, params[param])
                if PARSE_OK != gcfParseError:
                    print "Not able to add the result to the response"

            elif isinstance(params[param], list):
                gcfList = self._addList(param, params[param])
                stat = self.libGcf.GCFStruct_AppendFV(gcfRespHeader, gcfList)
                if PARSE_OK != stat:
                    print "Not able to add the list to the response"
            elif isinstance(params[param], dict):
                gcfList = self._addDict(param, params[param])
                stat = self.libGcf.GCFStruct_AppendFV(gcfRespHeader, gcfList)
                if PARSE_OK != stat:
                    print "Not able to add the list to the response"
            # TODO add other types

        gcfResp = c_char_p()
        gcfParseError = self.libGcf.GCFCreator_Create(
            gcfRespHeader, byref(gcfResp))
        if PARSE_OK != gcfParseError:
            print "Not able to create the response"
        else:
            print gcfResp.value
            iSendedBytes = self.libSac.sss_write(
                self.hSacConnection, gcfResp.value, len(gcfResp.value))
            if PARSE_OK == iSendedBytes:
                print "Response was not sent"

        self.libGcf.GCFCreator_FreeGCFMsg(gcfResp)
        self.libGcf.GCFStruct_FreeGCFStruct(gcfRespHeader)

    def sendEvent(self, eventString):
        eventString = "EVNT GDM NAME=" + eventString + ";"
        iSendedBytes = self.libSac.sss_write(
            self.hSacConnection, eventString, len(eventString))
        if PARSE_OK == iSendedBytes:
            print "Response was not sent"

    def _getFVValue(self, fv):
        if BT_INTEGER == fv.valueType:
            return(fv.value.integer)
        elif BT_STRING == fv.valueType:
            try:
                # fv's seems to encode all ints as strings...so try and convert
                # it to an int first.
                return int(cast(fv.value.string, c_char_p).value)
            except:
                return cast(fv.value.string, c_char_p).value
        else:
            return

    def _getFVList(self, fv):
        if BT_LIST == fv.valueType:
            firstItemName = cast(
                fv.value.list.contents.featureName, c_char_p).value
            if firstItemName == None:
                returnValue = []
            else:
                returnValue = {}  # collections.OrderedDict()
            try:
                currItem = fv.value.list.contents
                while 1:
                    currName = cast(currItem.featureName, c_char_p).value
                    if BT_INTEGER == currItem.valueType or BT_STRING == currItem.valueType:
                        if isinstance(returnValue, dict):
                            returnValue[currName] = self._getFVValue(currItem)
                        else:
                            returnValue.append(self._getFVValue(currItem))
                    elif BT_LIST == currItem.valueType:
                        if isinstance(returnValue, dict):
                            returnValue[currName] = self._getFVList(currItem)
                            try:
                                if isinstance(returnValue[currName], list) and len(returnValue[currName]) == 1 and (isinstance(returnValue[currName][0], str) or isinstance(returnValue[currName][0], int)):
                                    # The GCFresult seems to serialize single
                                    # items as a list with one item. If we have
                                    # that we'll just turn it into a single
                                    # item.
                                    returnValue[currName] = returnValue[
                                        currName][0]
                            except:
                                print "error"
                        else:
                            returnValue.append(self._getFVList(currItem))
                    # TODO add more types
                    currItem = currItem.next.contents

            except ValueError:
                # Can't figure out how to check for the null pointer so just
                # wait for the exception
                return returnValue
        else:
            return

    def _callHandler(self, parsedStruct):
        handlerName = cast(
            self.parsedStruct.contents.gcfheader.dest_addr.contents.name, c_char_p).value
        if handlerName in self.sysCalls:
            print "Calling " + handlerName
            parameters = []
            handler = self.sysCalls.get(handlerName)

            try:
                currFV = parsedStruct.contents.parameter.featureValue.contents
                while 1:
                    if BT_INTEGER == currFV.valueType or BT_STRING == currFV.valueType:
                        parameters.append(self._getFVValue(currFV))
                    elif BT_LIST == currFV.valueType:
                        try:
                            parameters.append(self._getFVList(currFV))
                        except:
                            parameters.append(None)
                    # TODO add more types
                    # item2 = currFV.value.list.contents.next
                    currFV = currFV.next.contents

            except ValueError:
                # Can't figure out how to check for the null pointer so just
                # wait for the exception
                pass
            except:
                print traceback.format_exc()

            print tuple(parameters)
            try:
                handler(*tuple(parameters))
            except Exception:
                # Print the stack but ignore the exception
                print traceback.format_exc()

        else:
            print handlerName + " system call not defined"

    def _handle_incoming_systemcalls(self):
        iErrorCodeRead = 1
        iReadBytes = c_int()
        #ReadText = create_string_buffer('\000' * self.iSizeReadbuffer)
        ReadText = create_string_buffer('\000' * self.iSizeReadbuffer)
        while 0 != iErrorCodeRead:
            self.parsedStruct = POINTER(GCFStruct)()
            iErrorCodeRead = self.libSac.sss_read(
                self.hSacConnection, byref(ReadText), self.iSizeReadbuffer, byref(iReadBytes))
            # msgString = "CALL GDM:118 ResultEngine_ResultProcess result_in={ { { start=1, end=2, conf=6000, fv={ _resultType={ 'SemanticResult' }, _version={ '2' }, _results={ { _domain={ 'UDE_slm' }, _probability={ '8285' }, _topics={ { _topic={ 'Addresses.NoAction' }, _probability={ '6084' }, _interpretations={ { _probability={ '5956' }, _slots={ { _name={ 'Destination.HouseNumber' }, _stringValue={ '600' }, _numberValue={ '61', '1002' }, _terminals={ '#_terminals0', '#_terminals1' } }, { _name={ 'Destination.Street' }, _stringValue={ 'Atlantic Ave' }, _numberValue={ '-1', '-1' }, _terminals={ '#_terminals2', '#_terminals3' } } } } } }, { _topic={ 'POIs.Navigate' }, _probability={ '2025' }, _interpretations={ { _probability={ '1983' }, _slots={ { _name={ 'Destination.HouseNumber' }, _stringValue={ '600' }, _numberValue={ '61', '1002' }, _terminals={ '#_terminals0', '#_terminals1' } }, { _name={ 'Destination.Street' }, _stringValue={ 'Atlantic Ave' }, _numberValue={ '-1', '-1' }, _terminals={ '#_terminals2', '#_terminals3' } } } } } }, { _topic={ 'Addresses.Navigate' }, _probability={ '154' }, _interpretations={ { _probability={ '151' }, _slots={ { _name={ 'Destination.HouseNumber' }, _stringValue={ '600' }, _numberValue={ '61', '1002' }, _terminals={ '#_terminals0', '#_terminals1' } }, { _name={ 'Destination.Street' }, _stringValue={ 'Atlantic Ave' }, _numberValue={ '-1', '-1' }, _terminals={ '#_terminals2', '#_terminals3' } } } } } } } }, { _domain={ 'CandC' }, _probability={ '444' }, _topics={ { _topic={ 'General.MoveFocus' }, _probability={ '444' }, _interpretations={ { _probability={ '379' }, _slots={ { _name={ 'RefCardinal' }, _stringValue={ '600' }, _numberValue={ '61', '1002' }, _terminals={ '#_terminals0', '#_terminals4' } } } } } } } }, { _domain={ 'Media_fm' }, _probability={ '519' }, _topics={ { _topic={ 'Songs.NoAction' }, _probability={ '519' }, _interpretations={ { _probability={ '346' }, _slots={ { _name={ 'Song.Artist' }, _stringValue={ 'john coltrane' }, _numberValue={ '1500085' } }, { _name={ 'Song.Album' }, _stringValue={ 'the heavyweight champion, the complete atlantic recordings' }, _numberValue={ '1400134' }, _terminals={ '#_terminals5' } }, { _name={ 'Song.Title' }, _stringValue={ 'like sonny' }, _numberValue={ '1100162' } }, { _name={ 'Correction' }, _stringValue={ '' }, _terminals={ '#_terminals6' } } } } } } } }, { _domain={ 'VAD_fst' }, _probability={ '317' }, _topics={ { _topic={ 'Contacts.Navigate' }, _probability={ '317' }, _interpretations={ { _probability={ '166' }, _slots={ { _name={ 'Contact.LastName' }, _stringValue={ 'Sykes' }, _numberValue={ '30588' }, _terminals={ '#_terminals7' } } } }, { _probability={ '150' } } } } } } }, _terminals={ { _conf={ '8714' }, _score={ '12878' }, _orthography={ '6' }, _beginTimeMs={ '1680' }, _beginTimeMs={ '1980' } }, { _conf={ '8334' }, _score={ '16358' }, _orthography={ 'hundred' }, _beginTimeMs={ '1980' }, _beginTimeMs={ '2316' } }, { _conf={ '6613' }, _score={ '25333' }, _orthography={ 'Atlantic street' }, _beginTimeMs={ '2316' }, _beginTimeMs={ '2808' } }, { _conf={ '6859' }, _score={ '21963' }, _orthography={ 'Ave street' }, _beginTimeMs={ '2808' }, _beginTimeMs={ '3252' } }, { _conf={ '3595' }, _score={ '29973' }, _orthography={ 'hundred' }, _beginTimeMs={ '1980' }, _beginTimeMs={ '2532' } }, { _conf={ '0' }, _score={ '147586' }, _orthography={ 'atlantic' }, _beginTimeMs={ '2328' }, _beginTimeMs={ '2820' } }, { _conf={ '0' }, _score={ '10897' }, _orthography={ 'no' }, _beginTimeMs={ '888' }, _beginTimeMs={ '1104' } }, { _conf={ '4748' }, _score={ '14716' }, _orthography={ 'Sykes' }, _beginTimeMs={ '1668' }, _beginTimeMs={ '1980' } } } } } } };"
            #msgString = "CALL GDM:118 ResultEngine_ResultProcess result_in={ { { start=1, end=2, conf=6000, fv={ _resultType={ 'SemanticResult' }, _version={ '2' } } } } };"
            msgString = ReadText.value
            msgString = msgString.replace("(1000)=", "=")
            # msgString = msgString.replace("#_terminals", "#/_terminals/")
            print "Worker thread Received following ", iReadBytes.value, "bytes ", msgString
            self.libGcf.GCFParse_Parse(
                self.gcfParserHandle, msgString, byref(self.parsedStruct))
            # its a CALL message.                print "Trying to call: ",
            # ReadText.value
            if MESSAGE_CALL == self.parsedStruct.contents.gcfheader.messageType:
                self._callHandler(self.parsedStruct)
            else:
                # We only handle CALL messages in this thread all others are
                # ignored for the moment
                print "Ignoring: ", msgString
