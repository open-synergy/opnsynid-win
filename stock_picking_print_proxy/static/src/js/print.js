function print_picking(instance, module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    module.PrintPicking  = Backbone.Model.extend({
        model: 'stock.picking',

        initialize: function(attributes){
            return this;
        },

        print_report: function(values){
            var self = this;
            var obj_users = new openerp.Model('res.users');
            var obj_proxy = new openerp.Model('proxy.backend');
            var user_id = instance.session.uid
            obj_users.query(["name","proxy_backend_id"])
                .filter([['id', '=', user_id]])
                .first()
                .then(function (user) {
                    if (user.proxy_backend_id){
                        proxy_id = user.proxy_backend_id[0]
                        obj_proxy.query(["backend_ip"])
                            .filter([['id', '=', proxy_id]])
                            .first()
                            .then(function (proxy) {
                                proxy = proxy.backend_ip
                                self.call_template(values, proxy);
                            }
                        )
                    }
                }
            );
        },

        call_template: function(values, proxy){
            var self = this;
            proxy_ip = proxy;
            if (proxy_ip){
                this.proxy_url = "http://"+ proxy_ip + ":8069"
                this.proxy = new module.ProxyDevice(this);
                this.proxy.connect(this.proxy_url)
                *_.each(values,function(value){
                    this.template = 'stock_picking_template'
                    self.proxy.print_receipt(QWeb.render(this.template,{
                        receipt: value, widget: self,
                    }
                    ));
                });
            }
        },
        print_picking: function(picking_ids) {
            var self = this;
            var pickingModel = new instance.web.Model(this.model);
            pickingModel.call('export_for_printing',[picking_ids]).then(function(picking){
                self.print_report(picking);
                return true;
            },function(err,event){
                event.preventDefault();
                console.log("Error")
            });
            return true
        },
    });

    instance.web.client_actions.add('stock_picking_print_proxy', 'instance.stock_picking_print_proxy.action');
    instance.stock_picking_print_proxy.action = function (instance, context) {
        this.picking_ids = []
        this.PrintPicking = new module.PrintPicking(this);

        if (context.context.picking_ids) this.picking_ids = context.context.picking_ids;
        this.PrintPicking.print_picking(this.picking_ids);
    };
};
