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
    let body = {};
    try {
      body = await context.request.json();
    } catch(e) {}

    // Call the verified live Python Playwright Engine
    const apiRes = await fetch("https://organic-parakeet-gx7rv659gjp5f97qv-8000.app.github.dev/api/fetch-primary", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await apiRes.text();

    return new Response(data, {
      status: apiRes.status,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: "Bridge connection error: " + (err.message || String(err))
    }), {
      status: 502,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }
}
