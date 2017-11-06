import http.server
import urllib.parse as urlparse
import sqlite3
import json
import search as search


class MyHttpSearch(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse.urlparse(self.path)
        path = url.path
        query_dict = urlparse.parse_qs(url.query)
        if path == '/':
            self._set_headers(200, 'ok', 'text/html')
            html = self.get_html_page_form()
            self.wfile.write(bytes(html, 'UTF-8'))
        elif path == '/result':
            if 'q' in query_dict.keys() and 'f' in query_dict.keys():
                if query_dict['f'][0] == 'json':
                    self._set_headers(200, 'ok', 'application/json')
                    self.wfile.write(bytes(json.dumps(self.get_data(query_dict['q'][0])), 'UTF-8'))
                elif query_dict['f'][0] == 'html':
                    self._set_headers(200, 'ok', 'text/html')
                    data = self.get_data(query_dict['q'][0])
                    html = self.get_html_page_result(query_dict['q'][0], data)
                    self.wfile.write(bytes(html, 'UTF-8'))
        elif path == '/search':
            if 'c_name' in query_dict.keys():
                self.send_response(302)
                self.send_header('Location', '/result?q=' + query_dict['c_name'][0] + '&f=html')
                self.end_headers()
        else:
            self._set_headers(200, 'ok', 'text/plain')
            self.wfile.write(bytes("you asked for " + path[1:], 'UTF-8'))

    def get_data(self, c_name):
        conn = sqlite3.connect("../data/scorelib.dat")
        cur = conn.cursor()
        data = search.getScores(cur, c_name)
        conn.commit()
        cur.close()
        conn.close()
        return data

    def get_html_page_result(self, c_name, data):
        template = """<html>
    <body>
        <h1>Composers and scores for text: %s</h1>
        <ul>"""

        for val in data:
            scores_items = ""
            for score in val['scores']:
                scores_items += """
                    <li>
                        %s
                    </li>
                """ % (score['name'], )

            scores = "<ul>%s</ul>" % (scores_items, )

            template += """
            <li>
                %s
                %s
            </li>
        """ % (val['composer'], scores)

        template += """
        </ul>
        <br>
        <br>
        <a href="/">Back to home</a>
    </body>
</html>"""

        html = template % (c_name, )
        return html

    def get_html_page_form(self):
        template = """
        <html>
            <body>
                <h1>Which composer you want? (substring)</h1>
                <form action="/search">
                    <input type="text" name="c_name">
                    <button type="submit">Search</button>
                </form>
            </body>
        </html>"""

        html = template % ( )
        return html

    def _set_headers(self, code, code_message, content_type=None):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(code, code_message)
        if content_type is not None:
            self.send_header('Content-type', content_type)
        self.end_headers()

if __name__ == "__main__":
    port = 8000
    print('Listening on localhost:%s' % port)
    server = http.server.HTTPServer(('', port), MyHttpSearch)
    server.serve_forever()

