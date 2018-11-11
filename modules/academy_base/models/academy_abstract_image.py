# -*- coding: utf-8 -*-
""" AcademyAbstractImage

This module contains a abstract class with the common behavior to add one
image in models which extends this
"""


# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api, tools


# pylint: disable=locally-disabled, R0903
class AcademyAbstractImage(models.AbstractModel):
    """ Abstract model with needed fields and behavior to manage item image

    Fields:
      image (Binary): loaded image
      image_medium (Binary): image auto-resized to 128x128
      image_small (Binary): image auto-resized to 64x64

    """

    _name = 'academy.abstract.image'
    _description = u'Academy common model image behavior'


    # ---------------------------- ENTITY FIELDS ------------------------------


    image = fields.Binary(
        string='Image',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='This field holds the image used as image for our customers, limited to 1024x1024px.'
    )


    # --------------------------- COMPUTED FIELDS -----------------------------


    # pylint: disable=locally-disabled, W0212
    image_medium = fields.Binary(
        string='Image (auto-resized to 128x128)',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help="Medium-sized image of the category. It is automatically " \
             "resized as a 128x128px image, with aspect ratio preserved. " \
             "Use this field in form views or some Kanban views.",
        compute=lambda self: self._get_image()
    )

    # pylint: disable=locally-disabled, W0212
    image_small = fields.Binary(
        string='Image (auto-resized to 64x64)',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help="Small-sized image of the category. It is automatically " \
             "resized as a 64x64px image, with aspect ratio preserved. " \
             "Use this field anywhere a small image is required.",
        compute=lambda self: self._get_image()
    )


    # ------------------ AUXILIARY FIELD METHOS AND EVENTS --------------------


    @api.multi
    @api.depends('image')
    def _get_image(self):
        """ Creates image_medium and image_small thumbs
        """

        for record in self:
            image = record.image
            if image:
                data = tools.image_get_resized_images(image)
                record.image_medium = data["image_medium"]
                record.image_small = data["image_small"]

