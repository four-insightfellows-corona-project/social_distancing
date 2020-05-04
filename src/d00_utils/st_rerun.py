#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 14:26:59 2020

@author: retrieved from https://gist.github.com/tvst/ef477845ac86962fa4c92ec6a72bb5bd.js
"""

import os
import sys
from streamlit.ScriptRequestQueue import RerunData
from streamlit.ScriptRunner import RerunException
from streamlit.server.Server import Server
import streamlit.ReportThread as ReportThread


src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)


def rerun():
    """Rerun a Streamlit app from the top!"""
    widget_states = _get_widget_states()
    raise RerunException(RerunData(widget_states))


def _get_widget_states():
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')
    # Got the session object!

    return session._widget_states