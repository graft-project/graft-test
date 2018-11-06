#!/usr/bin/env python3

from flask import Flask, json, request
import time
import datetime
import threading
#import nodetestdriver as NTD

class SuperNodeStub(Flask):
    def __init__(self, name):
        self.cnt_resp_to_collect = 0
        self.__resp_list = []
        Flask.__init__(self, name)
        self.after_request(self.on_after_req)
        self.__func_shutdown = None

    @property
    def cnt_resp_to_collect(self):
        return self.__cnt_resp_to_collect

    @cnt_resp_to_collect.setter
    def cnt_resp_to_collect(self, val):
        self.__cnt_resp_to_collect = val

    @property
    def resp_list(self):
        return self.__resp_list

    def collect_response(self, req):
        jo = json.loads(req.get_data(as_text = True))
        jo['flask_remote_addr'] = req.remote_addr
        self.resp_list.append(jo)

    def shutdowh_this_server(self):
        if self.__func_shutdown:
            self.__func_shutdown()

        #func_shutdown = request.environ.get('werkzeug.server.shutdown')
        #if func_shutdown is None:
        #    pass
        #    #raise RuntimeError('Not running with the Werkzeug Server')
        #else:
        #    func_shutdown()

    def stop(self):
        self.shutdowh_this_server()

    def complete(self):
        need = self.cnt_resp_to_collect
        done = len(self.resp_list)
        return (need <= done) if need else False

    def wait(self, wait_sec):
        time.sleep(wait_sec)

    def wait_till_complete(self, wait_sec = 0):
        now = datetime.datetime.now()
        dead_line = now + datetime.timedelta(seconds = wait_sec) if wait_sec else now + datetime.timedelta(minutes = 5)

        while not self.complete():
            time.sleep(1)
            need = self.cnt_resp_to_collect
            done = len(self.resp_list)
            print('wait for completeness: {}:{}'.format(done, need))
            if datetime.datetime.now() > dead_line:
                self.shutdowh_this_server()
                print('awating timw is out ...')
                break

    #@app.after_request
    def on_after_req(self, resp):
        self.collect_response(request)

        if self.__func_shutdown is None:
            self.__func_shutdown = request.environ.get('werkzeug.server.shutdown')

        if self.complete():
            #self.dump_response_into_file()
            self.shutdowh_this_server()

        need = self.cnt_resp_to_collect
        done = len(self.resp_list)
        print('\n  ##  on_after_req: {}:{}'.format(done, need))
        return resp

    def app_thread(self, host, port, out_file):
        #print('server started ...')
        #print('server started ..., output into {}'.format(out_file))
        #run_ctx['out-file'] = out_file
        #run_ctx['cnt-to-do'] = req_cnt
        #self.run(host = host, port = port)
        super().run(host = host, port = port)
        #Flask.__init__(self, name)

    #def run(self, host = NTD.ip_any_local, port = NTD.port_srpc, out_file = ''):
    def run(self, host = '0.0.0.0', port = 28690, out_file = ''):
        th_app = threading.Thread(name = 'flask-srv', target = self.app_thread, args = [host, port, out_file])
        time.sleep(1)
        th_app.start()
        #th_app.join()

class SNodeStub(SuperNodeStub):
    def __init__(self, the_test_name):
        name = '{}-snode-stub'.format(the_test_name)
        SuperNodeStub.__init__(self, name)

    def build_custom_default_response(self):
        json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
        resp = self.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
        resp.headers['Connection'] = 'close'
        return resp

        #name = the_test_name
#@app.route('/test')
#def on_test():
#    json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
#    resp = app.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
#    resp.headers['Connection'] = 'close'
#    return resp
#
#@app.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
#def on_supernode_announce():
#    json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
#    resp = app.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
#    #resp.headers['Content-Type'] = 'application/json'
#    resp.headers['Connection'] = 'close'
#    return resp
#
#@app.route('/dapi/v2.0/unicast', methods=['POST'])
#def on_unicast():
#    json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
#    resp = app.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
#    resp.headers['Connection'] = 'close'
#    return resp
#
#@app.route('/dapi/v2.0/broadcast', methods=['POST'])
#def on_broadcast():
#    json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
#    resp = app.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
#    resp.headers['Connection'] = 'close'
#    return resp
#
#@app.route('/dapi/v2.0/multicast', methods=['POST'])
#def on_multicast():
#    json_resp = {"jsonrpc":"2.0","id":0,"result":{"Status":0}}
#    resp = app.response_class(response = json.dumps(json_resp), status = 200, mimetype = 'application/json')
#    resp.headers['Connection'] = 'close'
#    return resp
#
#
#if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port = 28690)
#






    #app.logger.error('one more req')
    #dump_req_body_into_file(request)


#app = Flask(__name__)
#run_ctx = {'out-file': '', 'cnt-to-do': 0, 'cnt-done': 0, 'resp-list': []}

    #@resp_list.setter
    #def resp_list(self, val):
    #    self.__cnt_resp_to_collect = val

#def dump_response_into_file():
#    out_file = run_ctx['out-file']
#    if out_file:
#        jo = run_ctx['resp-list']
#        with open(out_file, "a") as of:
#            of.write(json.dumps(jo, indent = 2))
#    else:
#        print('out-file is not specified')
#
#def dump_req_body_into_file(req):
#    out_file = run_ctx['out-file']
#    if out_file:
#        jo = json.loads(req.get_data(as_text = True))
#        jo['flask_remote_addr'] = req.remote_addr
#        with open(out_file, "a") as of:
#            of.write(json.dumps(jo, indent = 2) + '\n')
#    else:
#        print('out-file is not specified')




#@app.before_request
#def log_request():
#    app.logger.debug("hdrs %s", request.headers)
#    app.logger.debug("body %s", request.get_data())
#    return None


#from typing import NamedTuple

#@app.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
#def on_supernode_announce():
#    return '{"jsonrpc":"2.0","id":0,"result":{"Status":0}}'

#@app.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
#def on_supernode_announce():
#    resp = Flask.make_response('{"jsonrpc":"2.0","id":0,"result":{"Status":0}}')
#    resp.headers['Content-Type'] = 'application/json'
#    resp.headers['Connection'] = 'close'
#    return resp

#output_file_name_env_var = 'flask-test-srv-out-file'
#class RunContext(NamedTuple):
    #out_file_name: str


        #fields = [k for k in req.form]

        #print('fileds: {}'.format(fields))

        #values = [req.form[k] for k in req.form]
        #data = dict(zip(fields, values))
        #with open(out_file, "a") as of:
        #    of.write(json.dumps(data))

        #with open(out_file, "a") as of:
        #    of.write(req.get_data(as_text = True) + '\n')
        #    of.write('src-host [{}] [{}]\n'.format(req.url, req.remote_addr))


#from http.server import BaseHTTPRequestHandler, HTTPServer
#from future.moves.urllib.parse import urlparse, parse_qs
#import json


        #t_webApp.setDaemon(True)

