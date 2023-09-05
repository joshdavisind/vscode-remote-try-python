# -----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# -----------------------------------------------------------------------------------------

import streamlit as st
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return app.send_static_file("index.html")


@app.route('/streamlit')
def streamlit():
    st.set_page_config(page_title="My Streamlit App")
    st.write("Hello, world!")


if __name__ == '__main__':
    app.run()