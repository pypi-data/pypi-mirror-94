# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from . import normalize
import logging
import os
from .modular_alert_builder.build_core import generate_alerts
import traceback


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs


def validate(alert, logger):
    try:
        fields = []
        if alert.get("entity"):
            for entity in alert.get("entity"):
                if entity.get("field") in fields:
                    raise Exception("Field names should be unique")
                else:
                    fields.append(entity.get("field"))

                if entity.get("type") in ["radio", "singleSelect"]:
                    if not entity.get("options"):
                        raise Exception(
                            "{} type must have options parameter".format(entity.get("type")))
                elif entity.get("options"):
                    raise Exception(
                        "{} type must not contain options parameter".format(entity.get("type")))

                if entity.get("type") in ["singleSelectSplunkSearch"]:
                    if not all([entity.get("search"), entity.get("valueField"), entity.get("labelField")]):
                        raise Exception("{} type must have search, valueLabel and valueField parameters".format(
                            entity.get("type")))
                elif any([entity.get("search"), entity.get("valueField"), entity.get("labelField")]):
                    raise Exception("{} type must not contain search, valueField or labelField parameter".format(
                        entity.get("type")))

    except:
        logger.error(traceback.format_exc())
        raise


def alert_build(schema_content, product_id, short_name, output_dir,sourcedir):

    # Initializing logger
    logging.basicConfig()
    logger = logging.getLogger('Alert Logger')
    logger = LoggerAdapter('ta="{}" Creating Alerts'.format(short_name),
                           logger)

    # Validation
    for alert in schema_content['alerts']:
        validate(alert, logger)

    # Get the alert schema with required structure
    envs = normalize.normalize(schema_content, product_id, short_name)
    pack_folder = os.path.join(sourcedir, 'arf_dir_templates', 'modular_alert_package')
    # Generate Alerts
    generate_alerts(pack_folder, output_dir, logger, envs)
