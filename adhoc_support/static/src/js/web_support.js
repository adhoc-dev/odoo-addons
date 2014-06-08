
openerp.web_support = function(openerp) {   
    
    var contract_provider = "";
    var contract_provider_url = "";
    var contract_provided = false;

    var QWeb = openerp.web.qweb,
    _t = openerp.web._t;
    
    openerp.web.Header = openerp.web.Header.extend({
        start: function() {
            this._super();
            
            var session_id = this.session.session_id;
            openerp.connection.rpc("/web_support/get_support_contract_information", {},
                    function(result){
                        if(result.correct){
                            contract_provided = true;
                            contract_provider = result.support_contract.contract_provider;
                            contract_provider_url = result.support_contract.contract_provider_url;
                            var footer = '<p class="oe_footer_powered">Powered by ' +
                                            '<a href="http://www.openerp.com">OpenERP</a> - ' +
                                            'Supported by <a href="' + contract_provider_url + 
                                            '" target="_blank">' + contract_provider +
                                            '</a></span><p>';
                            $('.oe_footer_powered').html(footer);
                        }
                    });
        }
    });
    
    
    openerp.web.CrashManager = openerp.web.CrashManager.extend({
        on_traceback: function(error) {
            var origin = openerp.connection.origin;
            var prefix = openerp.connection.prefix;
            var db_name = openerp.connection.db;
            
            if (openerp.connection.openerp_entreprise) {
                return this._super(error);
            }
            
            var error_dialog = new openerp.web.Dialog(this, {
                    title: _t("Error sending email"),
                    width: '50%',
                    height: '30%',
                    buttons: [{text: _t("Close"), click: function() { $(this).dialog("close"); }}]
                });
            
            var buttons;
            if(contract_provided){
                buttons = [
                    {text: _t("Send Error"), click: function() {
                        var params = {'error': error, 'origin': origin, 'prefix': prefix, 'db_name': db_name}
                        var inner_dialog_ref = $(this);
                        var ret = openerp.connection.rpc("/web_support/send_email", params,
                                            function(result){
                                                if(result.correct == false){
                                                    error_dialog.open();
                                                    var html = '<span class="support_error">' + result.error_message + '</span>'
                                                    error_dialog.$element.html(html);
                                                } else {
                                                    inner_dialog_ref.dialog("close");
                                                }
                                            });
                    }},
                    {text: _t("Close"), click: function() { $(this).dialog("close"); }}
                ]
            } else {
                 buttons = [
                    {text: _t("Close"), click: function() { $(this).dialog("close"); }}
                ]
            }
            
            var dialog = new openerp.web.Dialog(this, {
                title: "OpenERP " + _.str.capitalize(error.message),
                width: '80%',
                height: '50%',
                min_width: '800px',
                min_height: '600px',
                buttons: buttons
            }).open();
            
            dialog.$element.html(QWeb.render('CrashManagerError', {
                session: openerp.connection,
                error: error,
                support_name: contract_provider,
                support_link: contract_provider_url,
                contract_provided: contract_provided,
            }));
            
            $(".crash_manager_error_tabs").tabs();
        },
    });
}


