import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

let rootElement = document.getElementById('root')
if (!rootElement) {
  const createdRoot = document.createElement('div')
  createdRoot.id = 'root'
  document.body.appendChild(createdRoot)
  console.warn('Root element not found. Created and appended a new #root to document.body.')
  rootElement = createdRoot
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
