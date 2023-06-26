/** @odoo-module */

import { listView } from "@web/views/list/list_view";
import { CoopcycleOrdersListController } from "./coopcycle_orders_list_controller";
import { registry } from "@web/core/registry";

export const CoopcycleOrdersReportListView = {
    ...listView,
    Controller: CoopcycleOrdersListController,
    buttonTemplate: 'CoopcycleOrders.Buttons',
};

registry.category("views").add('coopcycle_orders_report_list', CoopcycleOrdersReportListView);
