// var instance = openerp;
openerp.stock_voucher = function (instance) {
    instance.web.ActionManager = instance.web.ActionManager.extend({
        ir_actions_report_dont_close_xml: function(action, options) {
            var self = this;
            instance.web.blockUI();
            action = _.clone(action);
            var eval_contexts = ([instance.session.user_context] || []).concat([action.context]);
            action.context = instance.web.pyeval.eval('contexts',eval_contexts);

            // iOS devices doesn't allow iframe use the way we do it,
            // opening a new window seems the best way to workaround
            if (navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
                var params = {
                    action: JSON.stringify(action),
                    token: new Date().getTime()
                };
                var url = self.session.url('/web/report', params);
                instance.web.unblockUI();
                $('<a href="'+url+'" target="_blank"></a>')[0].click();
                return;
            }
            var c = instance.webclient.crashmanager;
            return $.Deferred(function (d) {
                self.session.get_file({
                    url: '/web/report',
                    data: {action: JSON.stringify(action)},
                    complete: instance.web.unblockUI,
                    success: function(){
                        if (!self.dialog) {
                            options.on_close();
                        }
                        // La idea era tratar de usar esta funcion para que vuelva a recargar el form y tome los datos cambiados
                        // self.dialog_stop();
                        // this.inner_widget.views[this.inner_widget.active_view].controller.reload();
                        // return $.when();
                        d.resolve();
                    },
                    error: function () {
                        c.rpc_error.apply(c, arguments);
                        d.reject();
                    }
                });
            });
        },
    });
}
// openerp.your_module_name = function (instance) {
//     instance.web.ActionManager = instance.web.ActionManager.extend({

//         ir_actions_act_close_wizard_and_reload_view: function (action, options) {
//             if (!this.dialog) {
//                 options.on_close();
//             }
//             this.dialog_stop();
//             this.inner_widget.views[this.inner_widget.active_view].controller.reload();
//             return $.when();
//         },
//     });
// }
