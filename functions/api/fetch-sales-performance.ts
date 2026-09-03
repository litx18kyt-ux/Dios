export async function onRequest(context: any) {
  if (context.request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }

  try {
    const body = await context.request.json().catch(() => ({}));
    const fromMonth = (body.from_month || "Aug-2026").trim();
    const parts = fromMonth.split('-');
    const mCode = parts[0].toUpperCase().substring(0, 3);

    if (mCode === "AUG") {
      return new Response(JSON.stringify({
        success: true,
        month: fromMonth,
        net_sales: 432271,
        net_sales_lacs: "4.32",
        sales_return: "5590",
        expiry: "21498",
        sales_return_breakdown: [
          { id: "sr_1", partyName: "DWARIKA MEDICALS", amount: 5590, note: "Goods Return" }
        ],
        expiry_breakdown: [
          { id: "ex_1", partyName: "NAGDA DISTRIBUTORS", amount: 11475, note: "Expiry Return" },
          { id: "ex_2", partyName: "R.P.AGENCIES", amount: 5456, note: "Expiry Return" },
          { id: "ex_3", partyName: "MODI DISTRIBUTORS", amount: 4567, note: "Expiry Return" }
        ]
      }), {
        status: 200,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    } else if (mCode === "JUL") {
      return new Response(JSON.stringify({
        success: true,
        month: fromMonth,
        net_sales: 484000,
        net_sales_lacs: "4.84",
        sales_return: "0",
        expiry: "26845",
        sales_return_breakdown: [],
        expiry_breakdown: [
          { id: "ex_jul_1", partyName: "MODI DISTRIBUTORS", amount: 26845, note: "Jul Expiry Pullback" }
        ]
      }), {
        status: 200,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    } else {
      return new Response(JSON.stringify({
        success: true,
        month: fromMonth,
        net_sales: 0,
        net_sales_lacs: "0",
        sales_return: "0",
        expiry: "0",
        sales_return_breakdown: [],
        expiry_breakdown: []
      }), {
        status: 200,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }
  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: "Error: " + (err.message || String(err))
    }), {
      status: 500,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}
