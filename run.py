# -*- coding: utf-8 -*-

#
# * Copyright (c) 2009-2020. Authors: Cytomine SCRLFS.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on annotation "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */


# This is a sample of a software that can be run by the Cytomine platform using the Cytomine Python client (https://github.com/cytomine/Cytomine-python-client).

import os
import sys
import logging
import shutil

import cytomine
from cytomine.models import ImageInstanceCollection, JobData
from cytomine.models import ImageInstance, ImageInstanceCollection
from cytomine.models import Annotation, AnnotationCollection, Term
from cytomine.models import Project, ProjectCollection


# -----------------------------------------------------------------------------------------------------------
def run(cyto_job, parameters):

    job     = cyto_job.job
    project = cyto_job.project
    term_id = parameters.terms_list

    logging.info(f"Selected term is {term_id=}")

    term = Term()
    term.id = term_id
    term.fetch()

    annotations = AnnotationCollection()
    annotations.project = project.id
    annotations.fetch()
    nb_annotations = len(annotations)
    progress = 0
    progress_delta = 100 / nb_annotations
    
    for annotation in annotations:
        annotation.fetch()

        job.update(progress=progress, statusComment="Converting annotation {}...".format(annotation.id))

        new_annotation = Annotation()
        new_annotation.project = annotation.project
        new_annotation.image = annotation.image
        new_annotation.location = annotation.location
        new_annotation.term = annotation.term
        new_annotation.save()
        annotation.delete()
        
        logging.info("Finished processing annotation %s", annotation.id)
        progress += progress_delta

if __name__ == "__main__":
    logging.debug("Command: %s", sys.argv)

    with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
        run(cyto_job, cyto_job.parameters)