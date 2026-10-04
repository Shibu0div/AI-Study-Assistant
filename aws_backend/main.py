from s3 import upload_file 

from study_modes import generate_quiz

# upload_file(
#     r"data\Marvel.pdf",
#     BUCKET_NAME,
#     "documents/Marvel.pdf"
# )

result = generate_quiz(
    "Reproduction - The generating system"
)

print(result["answer"])
print("\nToken usage:")
print("Input:", result["input_tokens"])
print("Output:", result["output_tokens"])
print("Total:", result["total_tokens"])