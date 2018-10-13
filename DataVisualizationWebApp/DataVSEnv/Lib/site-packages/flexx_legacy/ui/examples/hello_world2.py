# -*- coding: utf-8 -*-
# doc-export: Main
"""
Simple hello world following the recommended style of writing apps,
using a custom widget that is populated in its ``init()``.
"""


from __future__ import print_function, absolute_import, with_statement, unicode_literals, division

from flexx import app, ui

class Main(ui.Widget):
    
    def init(self):
        
        self.b1 = ui.Button(text='Hello')
        self.b2 = ui.Button(text='World')

if __name__ == '__main__':
    m = app.launch(Main)
    app.run()
