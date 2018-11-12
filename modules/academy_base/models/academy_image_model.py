#pylint: disable=I0011,C0111,R0903,F0401
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, tools



class AcademyImageModel(models.AbstractModel):
    """ Abstract model with needed fields and behavior to manage item image

    Fields:
      image (Binary): loaded image
      image_medium (Binary): image auto-resized to 128x128
      image_small (Binary): image auto-resized to 64x64

    """

    _name = 'academy.image.model'


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

