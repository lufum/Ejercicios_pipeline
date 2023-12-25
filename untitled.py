import sys
from PyQt4 import QtCore, uic
from PyQt4.QtGui import *
import traceback
import logging

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = parent.textBrowser
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.setText(msg)
        print msg

    def write(self, m):
        pass


class gui_test (QWidget):
    def __init__(self, parent = None):
        super(gui_test, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.log_handler = QPlainTextEditLogger(self)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        print self.log_handler
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        self.do_btn.clicked.connect(self.di_hola)
    
    
    def test(self):
        err = ''
        err =  repr(traceback.format_exc())
        print "\n---", err
        """ exc_type, exc_value, exc_traceback = sys.exc_info()
        err = ''    
        for tr in traceback.format_exception(exc_type, exc_value, exc_traceback):
            err += tr """
        logging.debug(err)
        
    def di_hola(self):
        try:
            
            num_ls =  [1,3,5]
            out = str(num_ls [1])
            print "Hola" 
            self.disp_text.setText(out)
            logging.info(out)
            #self.test()
            
        except:
            self.test()
            """ exc_type, exc_value, exc_traceback = sys.exc_info()
            err = ''
            for tr in traceback.format_exception(exc_type, exc_value, exc_traceback):
                err += tr        
            self.disp_text.setText(err) """

if __name__ == '__main__':
    app =  QApplication (sys.argv)
    gui = gui_test()
    gui.show()
    sys.exit(app.exec_())
    