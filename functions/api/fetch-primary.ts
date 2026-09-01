export async function onRequestPost(context: any) {
  try {
    const body = await context.request.json();
    const fromMonth = body.from_month || "Aug-2026";
    const toMonth = body.to_month || "Aug-2026";
    const fyYear = body.fy_year || "2026-2027";

    const CBO_USER = "6958BANWARI";
    const CBO_PASS = "6958";

    // 1. Authenticate with CBO ERP (Direct HTTP Post)
    const loginUrl = "https://dios.myreporting.net/erp/login";
    const loginRes = await fetch(loginUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      },
      body: new URLSearchParams({
        "username": CBO_USER,
        "password": CBO_PASS,
        "txtUserName": CBO_USER,
        "txtPassword": CBO_PASS
      }),
      redirect: "manual"
    });

    const cookieHeader = loginRes.headers.get("set-cookie") || "";

    // 2. Fetch Direct Monthly Sales Summary Report
    const reportUrl = `https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=${fyYear}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1&fMonth=${fromMonth}&tMonth=${toMonth}`;

    const reportRes = await fetch(reportUrl, {
      headers: {
        "Cookie": cookieHeader,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });

    const html = await reportRes.text();

    // 3. Ultra-Fast Regex Parsing of the HTML Table
    const items: Array<{ name: string; qty: number; value: number }> = [];
    
    // Match table rows
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let match;

    while ((match = rowRegex.exec(html)) !== null) {
      const rowHtml = match[1];
      const cellMatches = rowHtml.match(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi);
      if (cellMatches && cellMatches.length >= 2) {
        const cleanCells = cellMatches.map(c => c.replace(/<[^>]+>/g, '').trim());
        const pName = cleanCells[0];
        
        if (pName && !pName.toUpperCase().includes("PRODUCT") && !pName.toUpperCase().includes("COUNT") && !pName.toUpperCase().includes("PRIMARY SALES")) {
          const qty = parseFloat(cleanCells[1]?.replace(/,/g, '') || "0") || 0;
          const val = parseFloat(cleanCells[2]?.replace(/,/g, '') || "0") || 0;
          
          if (pName.length > 2) {
            items.push({ name: pName, qty, value: val });
          }
        }
      }
    }

    const totalQty = items.reduce((sum, it) => sum + it.qty, 0);
    const totalVal = items.reduce((sum, it) => sum + it.value, 0);

    return new Response(JSON.stringify({
      success: true,
      from_month: fromMonth,
      to_month: toMonth,
      count: items.length,
      total_qty: totalQty,
      total_value: totalVal,
      items: items
    }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: err.message || "Failed to fetch from CBO"
    }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
