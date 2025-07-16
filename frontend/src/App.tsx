import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import MakeATale from './pages/MakeATale';
import About from './pages/About';
import Pricing from './pages/Pricing';
import FAQ from './pages/FAQ';

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/make" element={<MakeATale />} />
          <Route path="/about" element={<About />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/faq" element={<FAQ />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
