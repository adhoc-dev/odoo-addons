# -*- encoding: latin-1 -*-
import math
from osv import fields, osv
from openerp.tools.translate import _


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
        'pack_depth': fields.integer('Depth', required=True, help='Depth of the product if it is part of a pack.'),
        'pack_parent_line_id': fields.many2one('sale.order.line', 'Pack', help='The pack that contains this product.'),
        'pack_child_line_ids': fields.one2many('sale.order.line', 'pack_parent_line_id', 'Lines in pack', help=''),
    }

    _defaults = {
        'pack_depth': lambda *a: 0,
    }


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def copy(self, cr, uid, id, default=None, context=None):
        # Raise an error if lines are product pack because we can not copy pack
        # in a right way
        for line in self.browse(cr, uid, id, context=context). order_line:
            if line.pack_parent_line_id:
                raise osv.except_osv(
                    _('Error!'), _('You can not copy a sale order wich hast product packs!'))
        return super(sale_order, self).copy(
            cr, uid, id, default, context=context)

    def create(self, cr, uid, vals, context=None):
        result = super(sale_order, self).create(cr, uid, vals, context)
        self.expand_packs(cr, uid, [result], context)
        return result

    def write(self, cr, uid, ids, vals, context=None):
        result = super(sale_order, self).write(cr, uid, ids, vals, context)
        if 'order_line' in vals:
            self.expand_packs(cr, uid, ids, context)
        return result

    def expand_packs(self, cr, uid, ids, context={}, depth=1):

        def get_real_price(res_dict, product_id, qty, uom, pricelist):
            item_obj = self.pool.get('product.pricelist.item')
            price_type_obj = self.pool.get('product.price.type')
            product_obj = self.pool.get('product.product')
            template_obj = self.pool.get('product.template')
            field_name = 'list_price'

            if res_dict.get('item_id', False) and res_dict['item_id'].get(pricelist, False):
                item = res_dict['item_id'].get(pricelist, False)
                item_base = item_obj.read(cr, uid, [item], ['base'])[0]['base']
                if item_base > 0:
                    field_name = price_type_obj.browse(
                        cr, uid, item_base).field

            product = product_obj.browse(cr, uid, product_id, context)
            product_tmpl_id = product.product_tmpl_id.id

            product_read = template_obj.read(
                cr, uid, product_tmpl_id, [field_name], context)

            factor = 1.0
            if uom and uom != product.uom_id.id:
                product_uom_obj = self.pool.get('product.uom')
                uom_data = product_uom_obj.browse(cr, uid,  product.uom_id.id)
                factor = uom_data.factor
            return product_read[field_name] * factor

        if depth == 10:
            return
        updated_orders = []

        for order in self.browse(cr, uid, ids, context):

            fiscal_position = order.fiscal_position and self.pool.get(
                'account.fiscal.position').browse(cr, uid, order.fiscal_position, context) or False

            # The reorder variable is used to ensure lines of the same pack go right after their
            # parent.
            # What the algorithm does is check if the previous item had children. As children items
            # must go right after the parent if the line we're evaluating doesn't have a parent it
            # means it's a new item (and probably has the default 10 sequence number - unless the
            # appropiate c2c_sale_sequence module is installed). In this case we mark the item for
            # reordering and evaluate the next one. Note that as the item is not evaluated and it might
            # have to be expanded it's put on the queue for another iteration (it's simple and works well).
            # Once the next item has been evaluated the sequence of the item marked for reordering is updated
            # with the next value.

            sequence = -1
            reorder = []
            last_had_children = False
            lines_to_unlink = []
            for line in order.order_line:
                if last_had_children and not line.pack_parent_line_id:
                    reorder.append(line.id)
                    if line.product_id.pack_line_ids and not order.id in updated_orders:
                        updated_orders.append(order.id)
                    continue

                sequence += 1

                if sequence > line.sequence:
                    self.pool.get('sale.order.line').write(cr, uid, [line.id], {
                        'sequence': sequence,
                    }, context)
                else:
                    sequence = line.sequence

                if line.state != 'draft':
                    continue
                if not line.product_id:
                    continue

                # If pack was already expanded (in another create/write operation or in
                # a previous iteration) don't do it again.
                if line.pack_child_line_ids:
                    # Cambiamos esto para que se borren las lienas viejas y se
                    # creen nuevas
                    unlink_line_ids = [x.id for x in line.pack_child_line_ids]
                    lines_to_unlink.extend(unlink_line_ids)
                    # last_had_children = True
                    # continue
                last_had_children = False

                pack_price = 0.0
                # pack_discount = 0.0
                for subline in line.product_id.pack_line_ids:
                    sequence += 1

                    subproduct = subline.product_id
                    quantity = subline.quantity * line.product_uom_qty

                    if line.product_id.pack_fixed_price:
                        price = 0.0
                        discount = 0.0
                    else:
                        pricelist = order.pricelist_id.id
                        list_price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                                                                                  subproduct.id, quantity, order.partner_id.id, {
                            'uom': subproduct.uom_id.id,
                            'date': order.date_order,
                        })
                        price = list_price[pricelist]

                        # Added functionality for compatibility with
                        # product_visible_discount module
                        pricelist_obj = self.pool.get('product.pricelist')
                        pricelists = pricelist_obj.read(
                            cr, uid, [pricelist], ['visible_discount'])
                        new_list_price = get_real_price(
                            list_price, subproduct.id, quantity, subproduct.uom_id.id, pricelist)
                        discount = line.discount
                        if pricelists[0].has_key("visible_discount"):
                            if(len(pricelists) > 0 and pricelists[0]['visible_discount'] and list_price[pricelist] != 0):
                                discount += (new_list_price -
                                             price) / new_list_price * 100
                                price = new_list_price

                    # Obtain product name in partner's language
                    ctx = {'lang': order.partner_id.lang}
                    # subproduct_name = self.pool.get('product.product').browse(cr, uid, subproduct.id, ctx).name

                    tax_ids = self.pool.get('account.fiscal.position').map_tax(
                        cr, uid, fiscal_position, subproduct.taxes_id)
                    tax_id = [(6, 0, tax_ids)]

                    if subproduct.uos_id:
                        uos_id = subproduct.uos_id.id
                        uos_qty = quantity * subproduct.uos_coeff
                    else:
                        uos_id = False
                        uos_qty = quantity

                    # TODO no lo termine de implementar a esto porque lo complica, tal vez scanterra lo quiera
                    # If totalice price we sum the prices and set prices to 0
                    if line.product_id.totalice_price and not line.product_id.pack_fixed_price:
                        pack_price += (price * uos_qty)
                        # pack_discount += price
                        price = 0.0
                        discount = 0.0
                        tax_id = False

                    subproduct_name = self.pool.get('product.product').name_get(
                        cr, uid, [subproduct.id], context=ctx)[0][1]
                    if subproduct.description_sale:
                        subproduct_name += '\n' + subproduct.description_sale
                    vals = {
                        'order_id': order.id,
                        'name': '%s%s' % ('> ' * (line.pack_depth + 1), subproduct_name),
                        # 'name': '%s%s' % ('> '* (line.pack_depth+1), subproduct_name),
                        'sequence': sequence,
                        'delay': subproduct.sale_delay or 0.0,
                        'product_id': subproduct.id,
                        'procurement_id': line.procurement_id and line.procurement_id.id or False,
                        'price_unit': price,
                        'tax_id': tax_id,
                        'type': subproduct.procure_method,
                        'property_ids': [(6, 0, [])],
                        'address_allotment_id': False,
                        'product_uom_qty': quantity,
                        'product_uom': subproduct.uom_id.id,
                        'product_uos_qty': uos_qty,
                        'product_uos': uos_id,
                        'product_packaging': False,
                        'move_ids': [(6, 0, [])],
                        'discount': discount,
                        'number_packages': False,
                        'notes': False,
                        'th_weight': False,
                        'state': 'draft',
                        'pack_parent_line_id': line.id,
                        'pack_depth': line.pack_depth + 1,
                    }

                    # It's a control for the case that the nan_external_prices
                    # was installed with the product pack
                    if 'prices_used' in line:
                        vals['prices_used'] = line.prices_used

                    self.pool.get('sale.order.line').create(
                        cr, uid, vals, context)
                    if not order.id in updated_orders:
                        updated_orders.append(order.id)

                if line.product_id.totalice_price and not line.product_id.pack_fixed_price:
                    if quantity and int(quantity) != 0:
                        pack_price = pack_price / quantity
                    self.pool.get('sale.order.line').write(cr, uid, [line.id],
                                                           {'price_unit': pack_price}, context=context)

                for id in reorder:
                    sequence += 1
                    self.pool.get('sale.order.line').write(
                        cr, uid, [id], {'sequence': sequence}, context)

        # Borramos las lienas que se actualizan
        self.pool.get('sale.order.line').unlink(
            cr, uid, lines_to_unlink, context=context)

        # Sacamos esto porque es medio horrible
        # if updated_orders:
        # Try to expand again all those orders that had a pack in this iteration.
        # This way we support packs inside other packs.
        #     self.expand_packs(cr, uid, ids, context, depth+1)
        return
