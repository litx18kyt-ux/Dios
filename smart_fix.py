import subprocess

# 1. Restore pristine SalesPerformanceSheet.tsx from git repository
subprocess.run(["git", "checkout", "src/components/review/SalesPerformanceSheet.tsx"])

path = 'src/components/review/SalesPerformanceSheet.tsx'
with open(path, 'r') as f:
    content = f.read()

# 2. Add import
if 'unProgressionStore' not in content:
    content = content.replace(
        "import { memoryStore, PartyBreakdownItem, DEFAULT_STOCKISTS } from '../../data/memoryStore';",
        "import { memoryStore, PartyBreakdownItem, DEFAULT_STOCKISTS } from '../../data/memoryStore';\nimport { unProgressionStore } from '../../data/unProgressionStore';"
    )

# 3. Update formData initialization to persist in memoryStore
old_init = "const [formData, setFormData] = useState<Record<string, Record<string, string>>>(INITIAL_BASE);"
new_init = """const [formData, setFormData] = useState<Record<string, Record<string, string>>>(() => {
  if (!memoryStore.salesPerformanceData) {
    memoryStore.salesPerformanceData = INITIAL_BASE;
  }
  return memoryStore.salesPerformanceData;
});"""
if old_init in content:
    content = content.replace(old_init, new_init)

# 4. Update handleCellChange
old_change = """  const handleCellChange = (rowId: string, month: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [rowId]: {
        ...prev[rowId],
        [month]: value
      }
    }));
  };"""

new_change = """  const handleCellChange = (rowId: string, month: string, value: string) => {
    setFormData(prev => {
      const updated = {
        ...prev,
        [rowId]: {
          ...prev[rowId],
          [month]: value
        }
      };
      memoryStore.salesPerformanceData = updated;
      return updated;
    });
  };"""
if old_change in content:
    content = content.replace(old_change, new_change)

# 5. Add handleAutoSyncFromDataHub function before calculateCell
sync_func = """  const handleAutoSyncFromDataHub = () => {
    const gridData = unProgressionStore.getData();
    const newSecCurr: Record<string, string> = { ...(formData.sec_curr || {}) };
    const newClosingStock: Record<string, string> = { ...(formData.closing_stock || {}) };

    MONTHS.forEach(code => {
      const monthGrid = gridData[code] || {};
      let secTotalVal = 0;
      let closingTotalVal = 0;

      MASTER_PRODUCTS.forEach(p => {
        const item = monthGrid[p.sn];
        if (item) {
          secTotalVal += (item.netSec || 0) * p.pts;
          closingTotalVal += (item.closing || 0) * p.pts;
        }
      });

      if (secTotalVal > 0) {
        newSecCurr[code] = (secTotalVal / 100000).toFixed(2);
      }
      if (closingTotalVal > 0) {
        newClosingStock[code] = (closingTotalVal / 100000).toFixed(2);
      }
    });

    setFormData(prev => {
      const updated = {
        ...prev,
        sec_curr: newSecCurr,
        closing_stock: newClosingStock
      };
      memoryStore.salesPerformanceData = updated;
      return updated;
    });

    setStatusMsg('🎉 Successfully auto-synced Secondary 26-27 & Closing Stock from Data Hub!');
    setTimeout(() => setStatusMsg(null), 3500);
  };

  """
if 'handleAutoSyncFromDataHub' not in content:
    content = content.replace("const calculateCell = ", sync_func + "const calculateCell = ")

# 6. Add Auto-Sync button in UI before Upload SPO Excel
btn_target = '<label className="flex items-center gap-1.5 px-3.5 py-2 bg-blue-600'
btn_replacement = '''<button
        onClick={handleAutoSyncFromDataHub}
        className="flex items-center gap-1.5 px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-bold shadow-md shadow-cyan-600/20 transition cursor-pointer"
        title="Auto-sync Secondary 26-27 & Closing Stock from Data Hub"
      >
        <RefreshCw size={14} /> Auto-Sync Sec &amp; Stock
      </button>

      <label className="flex items-center gap-1.5 px-3.5 py-2 bg-blue-600'''
if 'Auto-Sync Sec' not in content:
    content = content.replace(btn_target, btn_replacement)

# 7. Update handleSave
old_save = "const handleSave = () => {"
new_save = "const handleSave = () => {\n    memoryStore.salesPerformanceData = formData;"
if "memoryStore.salesPerformanceData = formData;" not in content:
    content = content.replace(old_save, new_save)

with open(path, 'w') as f:
    f.write(content)
print("✅ Smart fix applied successfully!")
