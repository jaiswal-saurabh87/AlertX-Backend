import React, { useState } from 'react';
import { Upload, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

export default function DisasterDetection() {
  // Configure API base URL - change this to match your Flask server
  const API_BASE_URL = 'http://localhost:5000';
  
  const [file, setFile] = useState(null);
  const [confidence, setConfidence] = useState(0.5);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [processedData, setProcessedData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
    setProcessedData(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setResult(null);
    setError(null);
    setProcessedData(null);
    
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    
    setLoading(true);
    
    try {
      // Step 1: Upload file
      const uploadFormData = new FormData();
      uploadFormData.append('file', file);
      
      const uploadResponse = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: uploadFormData
      });
      
      if (!uploadResponse.ok) {
        throw new Error(`HTTP error! status: ${uploadResponse.status}`);
      }
      
      const uploadData = await uploadResponse.json().catch(e => {
        throw new Error('Invalid JSON response from upload endpoint');
      });
      
      if (uploadData.error) {
        throw new Error(uploadData.error);
      }
      
      // Step 2: Process file
      const processResponse = await fetch(`${API_BASE_URL}/api/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          filename: uploadData.filename,
          confidence_threshold: parseFloat(confidence)
        })
      });
      
      if (!processResponse.ok) {
        throw new Error(`HTTP error! status: ${processResponse.status}`);
      }
      
      const processData = await processResponse.json().catch(e => {
        throw new Error('Invalid JSON response from process endpoint');
      });
      
      if (processData.error) {
        throw new Error(processData.error);
      }
      
      // Display results
      setProcessedData(processData);
      setResult('Processing completed successfully!');
      
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-8 py-6">
            <h1 className="text-3xl font-bold text-white text-center">
              Human Detection in Disaster Scenarios
            </h1>
          </div>

          <div className="p-8">
            <p className="text-gray-600 mb-8 text-center">
              Upload an image or video to detect humans in disaster scenarios such as earthquakes, floods, building collapses, and fires.
            </p>

            <div className="space-y-6">
              {/* File Upload */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Select Image/Video File
                </label>
                <div className="relative">
                  <input
                    type="file"
                    id="file"
                    accept="image/*,video/*"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-3 file:px-4
                      file:rounded-lg file:border-0
                      file:text-sm file:font-semibold
                      file:bg-emerald-50 file:text-emerald-700
                      hover:file:bg-emerald-100
                      cursor-pointer border border-gray-300 rounded-lg
                      focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
                {file && (
                  <p className="mt-2 text-sm text-gray-500">
                    Selected: {file.name}
                  </p>
                )}
              </div>

              {/* Confidence Threshold */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Confidence Threshold: <span className="text-emerald-600 font-bold">{confidence}</span>
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={confidence}
                  onChange={(e) => setConfidence(parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>0.1</span>
                  <span>1.0</span>
                </div>
              </div>

              {/* Submit Button */}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-semibold py-3 px-6 rounded-lg
                  hover:from-emerald-600 hover:to-teal-700 transition-all duration-200 shadow-md hover:shadow-lg
                  disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed
                  flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload size={20} />
                    Upload and Process
                  </>
                )}
              </button>
            </div>

            {/* Result Messages */}
            {error && (
              <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}

            {result && (
              <div className="mt-6 bg-emerald-50 border border-emerald-200 rounded-lg p-4 flex items-start gap-3">
                <CheckCircle2 className="text-emerald-600 flex-shrink-0 mt-0.5" size={20} />
                <p className="text-emerald-800 text-sm font-medium">{result}</p>
              </div>
            )}

            {/* Processed Results */}
            {processedData && (
              <div className="mt-8 border-t pt-8">
                {processedData.type === 'image' && (
                  <div className="space-y-6">
                    <div className="bg-slate-50 rounded-lg p-6">
                      <h3 className="text-xl font-bold text-gray-800 mb-4">Processing Results</h3>
                      <p className="text-lg text-gray-700">
                        <span className="font-semibold">Humans detected:</span>{' '}
                        <span className="text-emerald-600 font-bold">{processedData.result.count}</span>
                      </p>

                      {processedData.result.count > 0 && (
                        <div className="mt-4">
                          <h4 className="font-semibold text-gray-800 mb-2">Detection Details:</h4>
                          <ul className="space-y-1">
                            {processedData.result.detections.map((detection, index) => (
                              <li key={index} className="text-gray-700">
                                Human {index + 1}: {Math.round(detection.confidence * 100)}% confidence
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-800 mb-3">Processed Image:</h4>
                      <img
                        src={`${API_BASE_URL}/processed/${processedData.result.processed_image}`}
                        alt="Processed"
                        className="w-full rounded-lg shadow-lg"
                      />
                    </div>
                  </div>
                )}

                {processedData.type === 'video' && (
                  <div className="space-y-6">
                    <div className="bg-slate-50 rounded-lg p-6">
                      <h3 className="text-xl font-bold text-gray-800 mb-4">Processing Results</h3>
                      <div className="space-y-2 text-gray-700">
                        <p>
                          <span className="font-semibold">Total frames processed:</span>{' '}
                          {processedData.result.total_frames}
                        </p>
                        <p>
                          <span className="font-semibold">Total human detections:</span>{' '}
                          <span className="text-emerald-600 font-bold">
                            {processedData.result.total_detections}
                          </span>
                        </p>
                        <p>
                          <span className="font-semibold">Average detections per frame:</span>{' '}
                          {processedData.result.avg_detections_per_frame.toFixed(2)}
                        </p>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-800 mb-3">Processed Video:</h4>
                      <video
                        controls
                        className="w-full rounded-lg shadow-lg"
                      >
                        <source
                          src={`${API_BASE_URL}/processed/${processedData.result.processed_video}`}
                          type="video/mp4"
                        />
                        Your browser does not support the video tag.
                      </video>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}