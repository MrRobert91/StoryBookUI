export default function Pricing() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-8">Planes y Precios</h1>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border rounded-lg p-6 flex flex-col items-center bg-white shadow">
          <h2 className="text-xl font-semibold mb-2">Plan Gratuito</h2>
          <p className="mb-4 text-gray-600 text-center">Genera un cuento de prueba para conocer la plataforma.</p>
          <span className="text-3xl font-bold mb-4">$0</span>
        </div>
        <div className="border rounded-lg p-6 flex flex-col items-center bg-white shadow">
          <h2 className="text-xl font-semibold mb-2">Pay as You Go</h2>
          <p className="mb-4 text-gray-600 text-center">10 cuentos por tan solo 10&nbsp;USD.</p>
          <span className="text-3xl font-bold mb-4">$10</span>
        </div>
      </div>
    </div>
  );
}
