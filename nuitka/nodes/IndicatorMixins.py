#     Copyright 2017, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Module for node class mixins that indicate runtime determined node facts.

These come into play after finalization only. All of the these attributes (and
we could use properties instead) are determined once or from a default and then
used like this.

"""


class MarkLocalsDictIndicatorMixin(object):
    def __init__(self):
        self.needs_locals_dict = False
        self.foreign_locals_dict = False

    def hasLocalsDict(self):
        return self.needs_locals_dict

    def markAsLocalsDict(self):
        self.needs_locals_dict = True

    def markAsForeignLocalsDict(self):
        self.foreign_locals_dict = True

    def hasForeignLocalsDict(self):
        return self.foreign_locals_dict


class MarkUnoptimizedFunctionIndicatorMixin(object):
    """ Mixin for indication that a function contains an exec or star import.

        These do not access global variables directly, but check a locals dictionary
        first, because they do.
    """

    def __init__(self, flags):
        self.unoptimized_locals = "has_exec" in flags
        self.unqualified_exec = "has_unqualified_exec" in flags
        self.exec_source_ref = None

    def markAsUnqualifiedExecContaining(self, source_ref):
        assert self.unqualified_exec

        # Let the first one win.
        if self.exec_source_ref is None:
            self.exec_source_ref = source_ref

    def isUnoptimized(self):
        return self.unoptimized_locals

    def isUnqualifiedExec(self):
        return self.unoptimized_locals and self.unqualified_exec

    def getExecSourceRef(self):
        return self.exec_source_ref


class MarkNeedsAnnotationsMixin(object):
    def __init__(self):
        self.needs_annotations_dict = False

    def markAsNeedsAnnotationsDictionary(self):
        """ For use during building only. Indicate "__annotations__" need. """
        self.needs_annotations_dict = True

    def needsAnnotationsDictionary(self):
        """ For use during building only. Indicate "__annotations__" need. """
        return self.needs_annotations_dict


class EntryPointMixin(object):
    def __init__(self):
        self.trace_collection = None

    def setTraceCollection(self, trace_collection):
        previous = self.trace_collection
        self.trace_collection = trace_collection
        return previous

    def getTraceCollection(self):
        return self.trace_collection
