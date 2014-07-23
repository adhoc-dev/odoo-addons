# encoding: utf-8
{
	"name" : "Product Pack",
	"version" : "0.1",
	"description" : """
Allows configuring products as a collection of other products. If such a product is added in a sale order, all the products of the pack will be added automatically (when storing the order) as children of the pack product.

The module has been made compatible with nan_external_prices and containts code to specifically handle when the module is available but they're still independent and there are no dependencies between them.

Developed for Trod y Avia, S.L.
        """,
	"author" : "NaN·tic",
	"website" : "http://www.NaN-tic.com",
	"depends" : [ 
		'sale'
	], 
	"category" : "Custom Modules",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [
		'security/ir.model.access.csv',
		'pack_view.xml'
	],
	"active": False,
	"installable": True
}
