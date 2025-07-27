# **Project 1A: Understand Your Document**

## **Adobe India Hackathon 2025: Connecting the Dots**

This project is a solution for Round 1A of the Adobe India Hackathon. It is a high-speed, accurate, and offline-first system designed to parse a PDF and extract its structural outline, including the Title and headings (H1, H2, H3), into a structured JSON format.

### **1\. Problem Statement**

The primary challenge of Round 1A is to build a program that can analyze the visual and structural layout of a PDF to create a hierarchical outline. This requires distinguishing between different levels of headings and body text without relying on pre-existing metadata, which is often missing or incorrect in real-world documents. The solution must be fast, efficient, and run entirely offline on a CPU.

### **2\. Our Approach: Heuristic-Based Font Profiling**

Our solution is built on a robust, heuristic-based approach that does not require any machine learning models, making it extremely lightweight and fast. The core idea is to create a "style profile" of the document and use that profile to classify text elements.

The workflow is as follows:

1. **Full Document Font Analysis**: The first step is to perform a quick scan of the entire PDF. We iterate through every text element on every page to build a comprehensive map of all unique font sizes and names used in the document. This gives us a statistical profile of the document's typography.  
2. **Hierarchical Style Inference**: With the profile complete, we apply a powerful heuristic: **headings are differentiated by font size**. We sort all unique font sizes in descending order.  
   * The **largest font size** is assumed to be the document's **Title**.  
   * The next three largest font sizes are designated as H1, H2, and H3, respectively.  
     This method is highly effective for the vast majority of professionally formatted documents.  
3. **Content Extraction and Classification**: We then perform a second pass through the document. This time, as we extract text blocks, we check the font size of each block against our inferred style hierarchy.  
   * If a text block's font size matches the Title size, it's marked as the title.  
   * If it matches an H1, H2, or H3 size, it is classified and recorded as a heading, along with its text content and page number.  
   * We apply simple cleaning rules to filter out irrelevant text, such as page numbers or short fragments that might share a heading's font size.  
4. **Structured JSON Output**: Finally, all the extracted information is compiled into a clean, valid JSON file that strictly adheres to the format specified in the challenge requirements.

This approach is not only compliant with all the performance and offline constraints but is also highly effective at creating accurate document outlines from a wide variety of PDF layouts.

### **3\. Libraries Used**

* **PyMuPDF (fitz)**: This is the only dependency. It is a highly efficient and fast library for parsing PDF files, extracting text, and, crucially, accessing detailed font information (size and name) for each text span.

### **4\. How to Build and Run the Solution**

The project is designed to be run inside a Docker container as per the hackathon requirements.

#### **Prerequisites**

* Docker installed and running on your machine.

#### **Build the Docker Image**

Navigate to the project's root directory in your terminal and run the following command to build the image:

docker build \-t adobe-hackathon-1a-solution .

#### **Run the Container**

Once the image is built, you can run the solution using the following command. This command mounts your local input directory into the container and mounts the container's output directory back to your local machine.

1. Place all your input PDFs in an input folder in the project root.  
2. Create an empty output folder in the project root.  
3. Run the container:

docker run \--rm \-v "$(pwd)/input:/app/input" \-v "$(pwd)/output:/app/output" adobe-hackathon-1a-solution

The container will start, automatically run the run.py script, process every PDF from /app/input, and generate a corresponding .json file for each one in /app/output, which will appear in your local output folder. The container will then stop.