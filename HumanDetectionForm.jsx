import React, { useState, useRef } from 'react';

const HumanDetectionForm = () => {
  // Form state
  const [file, setFile] = useState(null);
  const [confidence, setConfidence] = useState(0.5);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  
  // Refs
  const fileInputRef = useRef(null);

  // Handle file change
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
  };

  // Handle confidence change
  const handleConfidenceChange = (e) => {
    setConfidence(parseFloat(e.target.value));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Reset previous results and errors
    setResult(null);
    setError('');
    
    // Validate file
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    
    // Set submitting state
    setIsSubmitting(true);
    
    // In a real implementation, this would call your API
    // For this UI-only component, we'll simulate the process
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate successful response
      const mockResult = {
        type: file.type.startsWith('image') ? 'image' : 'video',
        result: file.type.startsWith('image') ? {
          count: Math.floor(Math.random() * 5) + 1,
          detections: Array.from({ length: Math.floor(Math.random() * 5) + 1 }, (_, i) => ({
            confidence: Math.random() * 0.5 + 0.5,
            class_name: 'Human'
          })),
          processed_image: 'processed_image.jpg'
        } : {
          total_frames: Math.floor(Math.random() * 1000) + 100,
          total_detections: Math.floor(Math.random() * 500) + 50,
          avg_detections_per_frame: Math.random() * 3 + 1,
          processed_video: 'processed_video.mp4'
        }
      };
      
      setResult(mockResult);
    } catch (err) {
      setError('Failed to process the file. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reset form
  const resetForm = () => {
    setFile(null);
    setConfidence(0.5);
    setResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-xl shadow-lg p-6 md:p-8">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">Human Detection in Disaster Scenarios</h1>
        <p className="text-gray-600 text-center mb-8">Upload an image or video to detect humans in disaster scenarios such as earthquakes, floods, building collapses, and fires.</p>
        
        {!result ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* File Upload */}
            <div className="space-y-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Select Image/Video File:
              </label>
              <input
                ref={fileInputRef}
                id="file"
                type="file"
                accept="image/*,video/*"
                onChange={handleFileChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              {file && (
                <p className="text-sm text-gray-500 mt-1">Selected: {file.name}</p>
              )}
            </div>
            
            {/* Confidence Threshold */}
            <div className="space-y-2">
              <label htmlFor="confidence" className="block text-sm font-medium text-gray-700">
                Confidence Threshold: <span className="font-semibold text-blue-600">{confidence.toFixed(2)}</span>
              </label>
              <input
                id="confidence"
                type="range"
                min="0.1"
                max="1.0"
                step="0.05"
                value={confidence}
                onChange={handleConfidenceChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0.1</span>
                <span>1.0</span>
              </div>
            </div>
            
            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
                {error}
              </div>
            )}
            
            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors ${
                isSubmitting 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
              }`}
            >
              {isSubmitting ? (
                <div className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </div>
              ) : (
                'Upload and Process'
              )}
            </button>
          </form>
        ) : (
          // Results Display
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-800">Processing Results</h2>
              <button
                onClick={resetForm}
                className="py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors"
              >
                Process Another
              </button>
            </div>
            
            {result.type === 'image' ? (
              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-medium text-gray-700 mb-2">Detection Summary</h3>
                  <p className="text-lg">Humans detected: <span className="font-bold text-blue-600">{result.result.count}</span></p>
                  
                  {result.result.count > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-700 mb-2">Detection Details:</h4>
                      <ul className="space-y-2">
                        {result.result.detections.map((detection, index) => (
                          <li key={index} className="flex justify-between items-center bg-white p-3 rounded border">
                            <span>Human {index + 1}</span>
                            <span className="font-medium">{(detection.confidence * 100).toFixed(0)}% confidence</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                
                <div className="text-center">
                  <h3 className="font-medium text-gray-700 mb-2">Processed Image</h3>
                  <div className="border-2 border-dashed border-gray-300 rounded-xl p-4 flex items-center justify-center bg-gray-50 min-h-[300px]">
                    <div className="text-center">
                      <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-500">Processed image would be displayed here</p>
                      <p className="text-xs text-gray-400 mt-1">Filename: {result.result.processed_image}</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white p-4 rounded border text-center">
                    <p className="text-sm text-gray-600">Total Frames</p>
                    <p className="text-2xl font-bold text-blue-600">{result.result.total_frames}</p>
                  </div>
                  <div className="bg-white p-4 rounded border text-center">
                    <p className="text-sm text-gray-600">Total Detections</p>
                    <p className="text-2xl font-bold text-blue-600">{result.result.total_detections}</p>
                  </div>
                  <div className="bg-white p-4 rounded border text-center">
                    <p className="text-sm text-gray-600">Avg. per Frame</p>
                    <p className="text-2xl font-bold text-blue-600">{result.result.avg_detections_per_frame.toFixed(2)}</p>
                  </div>
                </div>
                
                <div className="text-center">
                  <h3 className="font-medium text-gray-700 mb-2">Processed Video</h3>
                  <div className="border-2 border-dashed border-gray-300 rounded-xl p-4 flex items-center justify-center bg-gray-50 min-h-[300px]">
                    <div className="text-center">
                      <svg className="mx-auto h-12 w-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-500">Processed video would be displayed here</p>
                      <p className="text-xs text-gray-400 mt-1">Filename: {result.result.processed_video}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HumanDetectionForm;