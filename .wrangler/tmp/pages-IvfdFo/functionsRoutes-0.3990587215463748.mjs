import { onRequest as __api_download_primary_excel_ts_onRequest } from "/workspaces/Dios/functions/api/download-primary-excel.ts"
import { onRequest as __api_fetch_cbo_excel_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-cbo-excel.ts"
import { onRequest as __api_fetch_dcr_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-dcr.ts"
import { onRequest as __api_fetch_dcr_excel_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-dcr-excel.ts"
import { onRequest as __api_fetch_primary_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-primary.ts"
import { onRequest as __api_fetch_sales_performance_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-sales-performance.ts"

export const routes = [
    {
      routePath: "/api/download-primary-excel",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_download_primary_excel_ts_onRequest],
    },
  {
      routePath: "/api/fetch-cbo-excel",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_cbo_excel_ts_onRequest],
    },
  {
      routePath: "/api/fetch-dcr",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_dcr_ts_onRequest],
    },
  {
      routePath: "/api/fetch-dcr-excel",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_dcr_excel_ts_onRequest],
    },
  {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequest],
    },
  {
      routePath: "/api/fetch-sales-performance",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_sales_performance_ts_onRequest],
    },
  ]