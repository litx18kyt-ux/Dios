import { onRequest as __api_download_primary_excel_ts_onRequest } from "/workspaces/Dios/functions/api/download-primary-excel.ts"
import { onRequest as __api_fetch_primary_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-primary.ts"

export const routes = [
    {
      routePath: "/api/download-primary-excel",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_download_primary_excel_ts_onRequest],
    },
  {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequest],
    },
  ]