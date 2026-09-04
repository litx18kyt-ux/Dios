path = 'src/components/review/SalesPerformanceSheet.tsx'
with open(path, 'r') as f:
    code = f.read()

# Replace pre tag content with exact error message
old_pre = """          <pre className="text-xs bg-slate-950 p-4 rounded-xl overflow-auto font-mono text-rose-400 border border-rose-900">
            {String(this.state.error?.stack || this.state.error?.message || this.state.error)}
          </pre>"""

new_pre = """          <div className="bg-slate-950 p-4 rounded-2xl border border-rose-900 space-y-2">
            <div className="text-sm font-bold text-white font-mono">Exact Error Message:</div>
            <div className="text-sm text-rose-300 font-mono bg-rose-950/50 p-3 rounded-xl border border-rose-800">
              {String(this.state.error?.message || this.state.error)}
            </div>
          </div>"""

code = code.replace(old_pre, new_pre)

with open(path, 'w') as f:
    f.write(code)

print("✅ Error Boundary updated to show exact error message!")
