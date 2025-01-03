#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Initialize a storage object on import."""
import models.engine.file_storage as fs

storage = fs.FileStorage()

storage.reload()
