/** @odoo-module */

import { useBus } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { ListController } from "@web/views/list/list_controller";

export class CoopcycleOrdersListController  extends ListController {
    setup() {
        super.setup();
        if (this.props.context.inventory_mode || this.props.context.inventory_report_mode) {
            useBus(this.model, "record-updated", this.recordUpdated);
        }
    }

    /**
     * Handler called when the user clicked on the 'Sync with Coopcycle' button.
     * Opens wizard to display, at choice, the products inventory or a computed
     * inventory at a given date.
     */
    async onClickSyncCoopcycle() {
         const context = {
            active_model: this.props.resModel,
         };

         this.actionService.doAction({
            res_model: "coopcycle.order.query",
            views: [[false, "form"]],
            target: "new",
            type: "ir.actions.act_window",
            context: context
         })
    }
}