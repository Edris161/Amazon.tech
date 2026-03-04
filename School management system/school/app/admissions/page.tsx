import SectionTitle from "../../components/SectionTitle";
import Card from "../../components/Card";

export default function AdmissionsPage() {
  const steps = [
    "Submit application form",
    "Provide previous academic records",
    "Attend interview (if required)",
    "Receive admission confirmation",
  ];

  const requirements = [
    "Completed application form",
    "Birth certificate copy",
    "Previous school transcripts",
    "Passport size photographs",
  ];

  const fees = [
    { type: "Registration Fee", amount: "$100" },
    { type: "Tuition Fee (Primary)", amount: "$5000/year" },
    { type: "Tuition Fee (Middle)", amount: "$6000/year" },
    { type: "Tuition Fee (High)", amount: "$7000/year" },
  ];

  return (
    <div className="container mx-auto px-4 py-12 space-y-16">

      {/* Admission Process Steps */}
      <section>
        <SectionTitle title="Admission Process" />
        <div className="grid md:grid-cols-4 gap-6 mt-6">
          {steps.map((step, index) => (
            <Card
              key={index}
              title={`Step ${index + 1}`}
              description={step}
            />
          ))}
        </div>
      </section>

      {/* Requirements List */}
      <section>
        <SectionTitle title="Requirements" />
        <ul className="list-disc list-inside space-y-2 text-gray-700 mt-4">
          {requirements.map((req, index) => (
            <li key={index}>{req}</li>
          ))}
        </ul>
      </section>

      {/* Fee Structure */}
      <section>
        <SectionTitle title="Fee Structure" />
        <div className="overflow-x-auto mt-4">
          <table className="min-w-full border border-gray-300">
            <thead className="bg-blue-100">
              <tr>
                <th className="text-left px-4 py-2 border-b">Fee Type</th>
                <th className="text-left px-4 py-2 border-b">Amount</th>
              </tr>
            </thead>
            <tbody>
              {fees.map((fee, index) => (
                <tr key={index} className="hover:bg-gray-50 transition">
                  <td className="px-4 py-2 border-b">{fee.type}</td>
                  <td className="px-4 py-2 border-b">{fee.amount}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Download & Apply Buttons */}
      <section className="flex flex-col md:flex-row gap-4 justify-center mt-8">
        <a
          href="/documents/admission_form.pdf"
          className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition text-center"
          download
        >
          Download Admission Form
        </a>
        <a
          href="/apply"
          className="bg-secondary text-white px-6 py-3 rounded-lg hover:bg-blue-500 transition text-center"
        >
          Apply Now
        </a>
      </section>

    </div>
  );
}