export async function onRequestPost(context: any) {
  try {
    const body = await context.request.json();
    const fromMonth = (body.from_month || "Aug-2026").trim();
    const toMonth = (body.to_month || "Aug-2026").trim();
    const fyYear = body.fy_year || "2026-2027";

    const CBO_USER = "6958BANWARI";
    const CBO_PASS = "6958";

    // Common Headers
    const headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.9",
    };

    let cookies = "";

    // STEP 1: Direct Session Request to CBO
    const reportUrl = `https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=${fyYear}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1`;

    const getRes = await fetch(reportUrl, { headers });
    const setCookie = getRes.headers.get("set-cookie") || "";
    if (setCookie) {
      cookies = setCookie.split(";")[0];
    }

    const getHtml = await getRes.text();

    // Helper to extract ASP.NET hidden fields
    const extractField = (html: string, name: string) => {
      const regex = new RegExp(`name="${name}"[^>]*value="([^"]*)"`, 'i');
      const m = html.match(regex);
      return m ? m[1] : '';
    };

    const viewState = extractField(getHtml, '__VIEWSTATE');
    const viewStateGen = extractField(getHtml, '__VIEWSTATEGENERATOR');
    const eventValidation = extractField(getHtml, '__EVENTVALIDATION');

    // Helper to find Month Option Value
    const findOptionVal = (html: string, selectId: string, monthStr: string) => {
      const selectRegex = new RegExp(`<select[^>]*id="${selectId}"[\\s\\S]*?<\\/select>`, 'i');
      const selectMatch = html.match(selectRegex);
      if (!selectMatch) return monthStr;
      
      const optRegex = /<option[^>]*value="([^"]*)"[^>]*>([\s\S]*?)<\/option>/gi;
      let opt;
      while ((opt = optRegex.exec(selectMatch[0])) !== null) {
        if (opt[2].toLowerCase().includes(monthStr.toLowerCase()) || opt[2].toLowerCase().includes(monthStr.substring(0,3).toLowerCase())) {
          return opt[1];
        }
      }
      return monthStr;
    };

    const fromVal = findOptionVal(getHtml, 'MFDATE', fromMonth);
    const toVal = findOptionVal(getHtml, 'MTDATE', toMonth);

    // STEP 2: PostBack to generate the table
    const postData = new URLSearchParams();
    if (viewState) postData.append('__VIEWSTATE', viewState);
    if (viewStateGen) postData.append('__VIEWSTATEGENERATOR', viewStateGen);
    if (eventValidation) postData.append('__EVENTVALIDATION', eventValidation);
    postData.append('MFDATE', fromVal);
    postData.append('MTDATE', toVal);
    postData.append('btnGo', 'Go');
    postData.append('MGROUPING_ID', '0');
    postData.append('MDDLSUMMARY', '0');
    postData.append('MSTAFF_TYPE', '1');
    postData.append('MPA_ID', '6958');

    const postRes = await fetch(reportUrl, {
      method: 'POST',
      headers: {
        ...headers,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookies,
        'Referer': reportUrl
      },
      body: postData.toString()
    });

    const reportHtml = await postRes.text();

    // STEP 3: Parse HTML Table for all Product Rows
    const items: Array<{ name: string; qty: number; value: number }> = [];
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let match;

    while ((match = rowRegex.exec(reportHtml)) !== null) {
      const rowContent = match[1];
      const cellMatches = rowContent.match(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi);
      if (cellMatches && cellMatches.length >= 2) {
        const cells = cellMatches.map(c => c.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim());
        const pName = cells[0];

        if (pName && !pName.toUpperCase().includes("PRODUCT") && !pName.toUpperCase().includes("COUNT") && !pName.toUpperCase().includes("PRIMARY SALES") && !pName.toUpperCase().includes("TOTAL")) {
          const qty = parseFloat(cells[1]?.replace(/,/g, '') || "0") || 0;
          const val = parseFloat(cells[2]?.replace(/,/g, '') || "0") || 0;
          
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
      error: err.message || "Failed to fetch from CBO ERP"
    }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
