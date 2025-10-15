# 📸 Symptoms Sidebar - Visual Layout

## Desktop Layout (1400px+)

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                                                                                │
│  ┌─────────────────────────────────────────┐  ┌─────────────────────────────┐ │
│  │                                         │  │  📋 Available Symptoms      │ │
│  │   🏥 Medical Assistance Chatbot        │  │      [132]                  │ │
│  │   AI-Powered Disease Prediction        │  │                             │ │
│  │                                         │  │  ┌─────────────────────┐   │ │
│  │  ┌───────────────────────────────────┐ │  │  │ 🔍 Search symptoms  │   │ │
│  │  │ Describe Your Symptoms:           │ │  │  └─────────────────────┘   │ │
│  │  │                                   │ │  │                             │ │
│  │  │ fever, cough, headache           │ │  │  ┌─────────────────────┐   │ │
│  │  │                                   │ │  │  │ Itching             │   │ │
│  │  └───────────────────────────────────┘ │  │  ├─────────────────────┤   │ │
│  │  💡 Tip: Use medical terms...         │  │  │ Skin Rash           │   │ │
│  │                                         │  │  ├─────────────────────┤   │ │
│  │  ┌───────────────────────────────────┐ │  │  │ Nodal Skin...       │   │ │
│  │  │     🔍 Analyze Symptoms           │ │  │  ├─────────────────────┤   │ │
│  │  └───────────────────────────────────┘ │  │  │ Continuous Sneezing │   │ │
│  │                                         │  │  ├─────────────────────┤   │ │
│  │  ┌───────────────────────────────────┐ │  │  │ Shivering           │   │ │
│  │  │ 📋 ANALYSIS RESULTS               │ │  │  ├─────────────────────┤   │ │
│  │  │                                   │ │  │  │ Chills              │   │ │
│  │  │ ✓ Recognized Symptoms (3):       │ │  │  ├─────────────────────┤   │ │
│  │  │   • Fever                        │ │  │  │ Joint Pain          │   │ │
│  │  │   • Cough  ◄──────────────────┐  │ │  │  ├─────────────────────┤   │ │
│  │  │   • Headache                   │  │ │  │  │ Stomach Pain        │   │ │
│  │  │                               │  │ │  │  ├─────────────────────┤   │ │
│  │  │ 🌡️ SEVERITY: MODERATE         │  │ │  │  │ Acidity             │   │ │
│  │  │                               │  │ │  │  ├─────────────────────┤   │ │
│  │  │ 🔍 POSSIBLE DIAGNOSES         │  │ │  │  │ Ulcers On Tongue    │   │ │
│  │  │   1. Common Cold (68%)        │  │ │  │  ├─────────────────────┤   │ │
│  │  │   2. Bronchial Asthma (24%)   │  │ │  │  │ Muscle Wasting      │   │ │
│  │  │   3. Allergy (8%)             │  │ │  │  ├─────────────────────┤   │ │
│  │  └───────────────────────────────┘  │ │  │  │ Vomiting            │   │ │
│  │                                         │  │  ├─────────────────────┤   │ │
│  └─────────────────────────────────────┘  │  │ ...more symptoms...    │   │ │
│                                              │  └─────────────────────┘   │ │
│                                              └─────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Tablet Layout (768px - 1200px)

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │   🏥 Medical Assistance Chatbot                   │ │
│  │                                                    │ │
│  │   [Main Content Area]                             │ │
│  │   • Symptom Input                                 │ │
│  │   • Analyze Button                                │ │
│  │   • Results                                       │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  📋 Available Symptoms [132]                      │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │ 🔍 Search symptoms...                        │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │                                                    │ │
│  │  [Symptoms List - Max Height 400px]               │ │
│  │  • Itching                                        │ │
│  │  • Skin Rash                                      │ │
│  │  • Joint Pain                                     │ │
│  │  ...                                              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Mobile Layout (< 768px)

```
┌──────────────────────────┐
│                          │
│  🏥 Medical Chatbot     │
│                          │
│  ┌────────────────────┐ │
│  │ Describe symptoms  │ │
│  │                    │ │
│  └────────────────────┘ │
│                          │
│  [🔍 Analyze]           │
│                          │
│  ┌────────────────────┐ │
│  │ 📋 Symptoms [132]  │ │
│  │ ┌────────────────┐ │ │
│  │ │ 🔍 Search...   │ │ │
│  │ └────────────────┘ │ │
│  │ • Fever            │ │
│  │ • Cough            │ │
│  │ • Headache         │ │
│  │ ...                │ │
│  └────────────────────┘ │
│                          │
│  [Results Below]        │
│                          │
└──────────────────────────┘
```

## Interaction States

### Normal State
```
┌─────────────────────┐
│ Fever               │  ← Light gray background
└─────────────────────┘
```

### Hover State
```
┌─────────────────────┐
│ Fever            →  │  ← Slightly darker + slide right
└─────────────────────┘
```

### Active/Selected State
```
┌─────────────────────┐
│ Fever               │  ← Purple background + white text
└─────────────────────┘
```

### Search Filtered
```
┌─────────────────────────┐
│ 🔍 Search: "pain"       │
└─────────────────────────┘
    ↓
┌─────────────────────┐
│ Stomach Pain        │  ← Only matching symptoms shown
├─────────────────────┤
│ Chest Pain          │
├─────────────────────┤
│ Abdominal Pain      │
├─────────────────────┤
│ Back Pain           │
└─────────────────────┘
```

## Color Scheme

### Sidebar
- **Background**: White (#FFFFFF)
- **Border**: Shadow (0 20px 60px rgba(0,0,0,0.3))
- **Title**: Purple (#667eea)
- **Badge**: Purple background (#667eea) + White text

### Symptom Items
- **Normal**: Light gray (#f8f9fa)
- **Hover**: Medium gray (#e9ecef)
- **Active**: Purple (#667eea)
- **Text**: Dark gray (#333) / White (when active)
- **Border (left)**: Transparent → Purple on hover

### Search Box
- **Border**: Light gray (#e0e0e0)
- **Focus**: Purple (#667eea)
- **Background**: White
- **Placeholder**: Gray (#999)

### Scrollbar
- **Track**: Light gray (#f1f1f1)
- **Thumb**: Purple (#667eea)
- **Thumb (hover)**: Dark purple (#764ba2)

## Dimensions

### Desktop
- **Sidebar Width**: 320px
- **Max Height**: 90vh
- **Gap from Main**: 20px
- **Sticky Position**: Top 20px

### Mobile
- **Width**: 100%
- **Max Height**: 400px
- **Position**: Below main content

### Symptom Items
- **Padding**: 10px 12px
- **Border Radius**: 8px
- **Border Left**: 3px
- **Font Size**: 0.9em

### Search Box
- **Padding**: 10px
- **Border**: 2px
- **Border Radius**: 8px
- **Margin Bottom**: 15px

## Animations

### Hover Effect
```css
transition: all 0.2s ease
transform: translateX(5px)
```

### Click Feedback
```css
- Add 'active' class
- Wait 500ms
- Remove 'active' class
```

### Scroll
```css
scroll-behavior: smooth
```

## Typography

### Sidebar Title
- **Font Size**: 1.3em
- **Font Weight**: 600
- **Color**: #667eea

### Symptom Count Badge
- **Font Size**: 0.8em
- **Font Weight**: 600
- **Padding**: 3px 10px

### Symptom Items
- **Font Size**: 0.9em
- **Font Weight**: Normal
- **Line Height**: 1.4

### Search Placeholder
- **Font Size**: 0.9em
- **Font Style**: Italic
- **Color**: #999

## Accessibility Features

- **Click targets**: Minimum 44px height
- **Color contrast**: WCAG AA compliant
- **Keyboard navigation**: Tab through symptoms
- **Screen reader**: Proper ARIA labels
- **Focus indicators**: Visible focus states
- **Touch targets**: Optimized for mobile

## Performance Optimizations

- **Lazy loading**: Symptoms loaded once
- **Virtual scrolling**: Not implemented (list is short enough)
- **Debouncing**: Search is instant (no delay needed)
- **Caching**: Symptoms cached in memory
- **CSS**: Hardware accelerated transforms

---

This layout provides an intuitive, accessible, and performant symptom selection experience across all devices! 🎨✨
