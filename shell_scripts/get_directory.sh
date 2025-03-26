tree -I 'node_modules|.git|__pycache__' > prompt.txt
echo -e "\n" >> prompt.txt

for file in $(find . -name "*.py" | head -n 5); do
  echo "--- FILE: $file ---" >> prompt.txt
  cat "$file" >> prompt.txt
  echo -e "\n" >> prompt.txt
done

echo "DONE" >> prompt.txt