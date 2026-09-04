import os

path = 'src/components/review/SalesPerformanceSheet.tsx'
with open(path, 'r') as f:
    code = f.read()

# Wrap SalesPerformanceSheet with Error Boundary
error_boundary_code = '''
import React, { Component, ErrorInfo, ReactNode } from 'react';

class SalesPerformanceErrorBoundary extends Component<{children: ReactNode}, {hasError: boolean, error: any}> {
  state = { hasError: false, error: null };
  static getDerivedStateFromError(error: any) {
    return { hasError: true, error };
  }
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("SalesPerformance Error:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 bg-rose-950/90 border-2 border-rose-500 text-rose-200 rounded-3xl space-y-3 shadow-2xl m-4">
          <h3 className="font-bold text-lg flex items-center gap-2">⚠️ Sales Performance Crash Error</h3>
          <p className="text-xs text-rose-300">Yeh error blank screen ki vajah ban raha tha:</p>
          <pre className="text-xs bg-slate-950 p-4 rounded-xl overflow-auto font-mono text-rose-400 border border-rose-900">
            {String(this.state.error?.stack || this.state.error?.message || this.state.error)}
          </pre>
          <button 
            onClick={() => { localStorage.clear(); window.location.reload(); }}
            className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-bold cursor-pointer"
          >
            Clear Memory &amp; Reload App
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export const SalesPerformanceSheet: React.FC = () => {
  return (
    <SalesPerformanceErrorBoundary>
      <SalesPerformanceContent />
    </SalesPerformanceErrorBoundary>
  );
};

const SalesPerformanceContent: React.FC = () => {
'''

# Replace export const SalesPerformanceSheet: React.FC = () => { with Error Boundary version
code = code.replace("export const SalesPerformanceSheet: React.FC = () => {", error_boundary_code)

with open(path, 'w') as f:
    f.write(code)

print("✅ Error Boundary added to SalesPerformanceSheet.tsx!")
