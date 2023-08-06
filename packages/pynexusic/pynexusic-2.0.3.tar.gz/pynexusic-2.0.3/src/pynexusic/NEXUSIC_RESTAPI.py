import requests
import base64
import datetime
import traceback

SCRIPT_VERSION = '2.0.3'

############################# NEXUS REST API V2 Functions ############################
class NEXUSIC_REST():
    def __init__(self, icweb_uri, authentication_type='APIKEY',
                 username=None, password=None, api_key=None,
                 max_attempts=1, timeout=None, verbose=False, verify=True):
        self.icweb_uri = icweb_uri
        self.authentication_type = authentication_type

        self.api_key = api_key
        self.username = username
        self.password = password

        self.max_attempts = max_attempts
        self.timeout = timeout   # TODO: To be added to the REST calls
        self.verbose = verbose
        self.verify = verify

        if authentication_type == 'APIKEY':
            if self.api_key != None:
                self.key_64 = self.generate_base64(api_key)
            else:
                raise Exception('API Key is not valid, please provide a valid API Key')
        elif authentication_type == 'BASIC':
            if self.username != None or self.password != None:
                self.key_64 = self.generate_base64(self.username + ':' + self.password)
            else:
                raise Exception('Username and/or password are not valid, please provide a valid username/password')

        self.hash = self.generate_hash()

    ######################################################################################
    def generate_base64(self, value):
        return str(base64.b64encode(bytes(value, 'utf-8')), "utf-8")

    ######################################################################################
    def generate_hash(self, verbose=False):
        result, result_code = self.authenticate(verbose=verbose)

        if result_code == 200:
            return result.get('hash')
        else:
            errorMsg = traceback.format_exc()
            raise Exception(result + '\n' + errorMsg)

    ######################################################################################
    def validate_and_return_response(self, response, message, raw=False):
        if response.status_code == 200:
            if raw:
                return response.raw, response.status_code
            else:
                return response.json(), response.status_code
        else:
            return str(message) + str(response.status_code) + ': ' + str(response.text), \
                   response.status_code

    ######################################################################################
    def authenticate(self, verbose=False):
        if self.verbose or verbose:
            print('Authenticating with NEXUS IC...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/security/login'
        res = requests.get(uri, headers={'Authorization': self.authentication_type + ' ' + self.key_64},
                           verify=self.verify)

        return self.validate_and_return_response(res, 'Authentication error ')

    ######################################################################################
    def getVersion(self, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting NEXUS IC version...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/version' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get version error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.getVersion(current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getTable(self, tableName, xFilter=None, pageSize=None, current_attempt=1,
                 verbose=False):
        if self.verbose or verbose:
            print('Getting ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        if pageSize == None:
            uri = baseURI + '/bo/' + tableName + '/' + '?hash=' + self.hash
        else:
            uri = baseURI + '/bo/' + tableName + '/' + '?pageSize=' + str(pageSize) + '&hash=' + self.hash

        try:
            if xFilter != None:
                res = requests.get(uri, headers={'X-NEXUS-Filter': xFilter}, verify=self.verify)
            else:
                res = requests.get(uri, verify=self.verify)

            result, result_code = self.validate_and_return_response(res, 'Get ' + tableName + ' table error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.getTable(tableName, xFilter=xFilter, pageSize=pageSize,
                                    current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def deleteRecord(self, tableName, keyValue, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Deleting from ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableName + '/' + str(keyValue) + '/' + '?hash=' + self.hash

        try:
            res = requests.delete(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Delete ' + tableName + ' table error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.deleteRecord(tableName, keyValue, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getMultimedia(self, rd_id, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting multimedia: ' + str(rd_id) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        xFilter = str(rd_id) + '/File_Data'
        uri = baseURI + '/bo/' + 'Repository_Data' + '/' + xFilter + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, stream=True, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get multimeida error ', raw=True)
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.getMultimedia(rd_id, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    # V6.6 only
    def getDashboard(self, dashboard_Name, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Generating NEXUS IC dashboard...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + dashboard_Name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/dashboard/' + str(rt_id) + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get ' + dashboard_Name + ' error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.getDashboard(dashboard_Name, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def generateReport(self, report_name, recipient, format='XLSX', current_attempt=1,
                       verbose=False):
        if self.verbose or verbose:
            print('Generating NEXUS IC report...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + report_name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        # Generate report
        uri = baseURI + '/web/generateReport'
        uri += '?key=' + str(rt_id) + '&format=' + format + '&recipient=' + recipient + '&hash=' + self.hash

        try:
            res = requests.post(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Generate ' + report_name + ' report error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.generateReport(report_name, recipient, format=format,
                                          current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execFunction(self, functionName, parameters=None, current_attempt=1,
                     verbose=False):
        if self.verbose or verbose:
            print('Executing ' + str(functionName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/function/' + functionName
        uri += '/' + '?hash=' + self.hash

        try:
            res = requests.post(uri, json=parameters, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Execute function ' + functionName + ' error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.execFunction(functionName, parameters=parameters,
                                        current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execUpdate(self, tableName, tableID, body, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Updating ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableName + '/' + tableID
        uri += '?hash=' + self.hash

        try:
            res = requests.post(uri, json=body, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Updating ' + tableName + ' error ')
            return result, result_code
        except Exception as e:
            if 'An existing connection was forcibly closed by the remote host' in str(e):
                current_attempt += 1
                if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                    self.hash = self.generate_hash()
                    return self.execUpdate(tableName, tableID, body,
                                      current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)


######################################################################################
################################### Start Script #####################################
if __name__ == '__main__':
    baseURI = ''
    apiKey = ''

    startTime = datetime.datetime.now()

    ## Program start here

    ## End of program

    endTime = datetime.datetime.now()
    elapsedTime = endTime - startTime

    print('NEXUS IC REST API actions completed.....runtime: %s' % (str(elapsedTime)))


