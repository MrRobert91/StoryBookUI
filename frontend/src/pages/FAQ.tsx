export default function FAQ() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-8">Preguntas Frecuentes</h1>
      <div className="space-y-4">
        <details className="bg-white rounded shadow p-4">
          <summary className="font-medium cursor-pointer">¿Qué es Make a Tale?</summary>
          <p className="mt-2 text-gray-700">
            Es una aplicación web que genera cuentos infantiles personalizados a
            partir de una breve descripción proporcionada por el usuario.
          </p>
        </details>
        <details className="bg-white rounded shadow p-4">
          <summary className="font-medium cursor-pointer">¿Necesito instalar algo?</summary>
          <p className="mt-2 text-gray-700">No, la plataforma funciona directamente desde tu navegador.</p>
        </details>
        <details className="bg-white rounded shadow p-4">
          <summary className="font-medium cursor-pointer">¿Cuánto cuesta el servicio?</summary>
          <p className="mt-2 text-gray-700">
            Puedes probarlo gratis con un cuento. Luego puedes adquirir 10 cuentos por 10&nbsp;USD en el plan Pay as You Go.
          </p>
        </details>
        <details className="bg-white rounded shadow p-4">
          <summary className="font-medium cursor-pointer">¿Puedo cancelar en cualquier momento?</summary>
          <p className="mt-2 text-gray-700">Sí, no existen contratos ni compromisos a largo plazo.</p>
        </details>
      </div>
    </div>
  );
}
