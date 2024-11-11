import React from 'react';
import { IClassifiedData, ILabResult } from '../models/poc';


const SamplePatientChart: React.FC<{ patient: IClassifiedData }> = ({ patient }) => {

  return (
    <div className="p-6 bg-gray-50 rounded-lg shadow-md">
      <h2 className="mt-0 mb-5 flex justify-center text-2xl font-semibold">Sample Patient Chart</h2>
      <div className="grid grid-cols-2 gap-6">
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Patient Information</h3>
          <p><strong>Name:</strong> {patient.name}</p>
          <p><strong>Age:</strong> {patient.age}</p>
          <p><strong>Gender:</strong> {patient.gender}</p>
          <p><strong>Contact:</strong> {patient.contactInfo}</p>
          <p><strong>Insurance:</strong> {patient.insurance}</p>
        </div>

        {/* Medical History */}
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Medical History</h3>
          <ul>
            {patient.medicalHistory?.map((history: string, index: number) => (
              <li key={index}>- {history}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mt-6">
        {/* Allergies */}
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Allergies</h3>
          <ul>
            {patient.allergies?.map((allergy: string, index: number) => (
              <li key={index}>- {allergy}</li>
            ))}
          </ul>
        </div>

        {/* Diagnoses */}
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Diagnoses</h3>
          <ul>
            {patient.diagnoses?.map((diagnosis: string, index: number) => (
              <li key={index}>- {diagnosis}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mt-6">
        {/* Prescriptions */}
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Prescriptions</h3>
          <ul>
            {patient.prescriptions?.map((prescription: string, index: number) => (
              <li key={index}>- {prescription}</li>
            ))}
          </ul>
        </div>

        {/* Lab Results */}
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Lab Results</h3>
          <table className="min-w-full table-auto">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left">Test Name</th>
                <th className="px-4 py-2 text-left">Result</th>
                <th className="px-4 py-2 text-left">Date</th>
              </tr>
            </thead>
            <tbody>
              {patient.labResults?.map((result: ILabResult, index: number) => (
                <tr key={index} className="border-t">
                  <td className="px-4 py-2">{result.testName}</td>
                  <td className="px-4 py-2">{result.result}</td>
                  <td className="px-4 py-2">{result.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6 mt-6">
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Reason for Visit</h3>
          <p>{patient.reasonForVisit}</p>
        </div>

        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Symptoms</h3>
          <p>{patient.symptoms}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 mt-6">
        <div className="p-4 border border-gray-300 rounded-md hover:bg-blue-100 transition duration-300">
          <h3 className="text-lg font-medium">Notes</h3>
          <p>{patient.notes}</p>
        </div>
      </div>
    </div>
  );
};

export default SamplePatientChart;
