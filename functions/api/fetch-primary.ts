export async function onRequestPost(context: any) {
  try {
    const body = await context.request.json();

    // Call Render Playwright Bot Server from Cloudflare backend
    const renderResponse = await fetch("https://dios-xmo1.onrender.com/api/fetch-primary", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const responseText = await renderResponse.text();

    return new Response(responseText, {
      status: renderResponse.status,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: "Render Bot Server is currently waking up or unreachable. Please try again in 15 seconds."
    }), {
      status: 502,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
