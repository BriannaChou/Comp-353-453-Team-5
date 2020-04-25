#!/bin/python
import sys
sys.path.insert(0, './chat_app')

from app import app

if __name__ == '__main__':
	app.run(debug=True)
