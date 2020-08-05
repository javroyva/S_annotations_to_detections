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
from cytomine.models import Annotation, AnnotationCollection
from cytomine.models import Ontology, OntologyCollection
from cytomine.models import Term, TermCollection
from cytomine.models import Project, ProjectCollection

# -----------------------------------------------------------------------------------------------------------
def run(cyto_job, parameters):

    job        = cyto_job.job
    project_id = cyto_job.project
    term_id    = parameters.terms_list

    logging.info(f"########### Parameters = {str(parameters)}")
    logging.info(f"########### Term {str(term_id)}")
    logging.info(f"########### Project {str(project_id)}")

    annotations = AnnotationCollection()
    annotations.project = project_id
    annotations.terms   = [term_id]
    annotations.fetch()

    progress = 0
    progress_delta = 1.0 / (1.50 * len(annotations))

    job.update(progress=progress, statusComment=f"Converting annotations from project {project_id}")

    new_annotations = AnnotationCollection()
    for a in annotations:
        if a.location is None:
            a.fetch()
        new_annotations.append(Annotation(a.location, a.image, a.term, a.project))
    new_annotations.save(chunk = None)

    job.update(progress=0.25, statusComment=f"Deleting old annotations...")

    for a in annotations:
        a.delete()
        progress += progress_delta
        job.update(progress=progress)

if __name__ == "__main__":
    logging.debug("Command: %s", sys.argv)

    with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
        run(cyto_job, cyto_job.parameters)