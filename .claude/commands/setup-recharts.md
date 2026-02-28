# Install Recharts for New Slides

Run this ONCE before building slides 6–17. This installs Recharts alongside the existing ECharts (which remains for slides 3–5).

## Steps

1. Install recharts:
```bash
cd web && npm install recharts
```

2. Verify the install succeeded:
```bash
cd web && npm ls recharts
```

3. Verify the build still works:
```bash
cd web && npm run build
```

That's it. Recharts is now available for import in any slide component:

```jsx
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, PieChart, Pie, Legend
} from 'recharts'
```

## What Changed

- `recharts` added to `web/package.json` dependencies
- ECharts is NOT removed (slides 3–5 still use it)
- No config changes needed — Recharts works with Vite out of the box

## Next Step

Run `.claude/commands/batch-1-slides-6-8.md` to start building slides 6–8 with Recharts.
