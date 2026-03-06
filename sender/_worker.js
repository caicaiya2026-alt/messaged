// Cloudflare Pages Functions - 可选，用于处理动态请求

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 可以在这里添加API端点或其他动态功能
    if (url.pathname === '/api/status') {
      return new Response(JSON.stringify({
        status: 'ok',
        timestamp: new Date().toISOString()
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // 默认返回静态文件
    return env.ASSETS.fetch(request);
  }
};
