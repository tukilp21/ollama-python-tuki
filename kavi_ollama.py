self.model_name = qwen2.5vl:32b
  masked_image = get_masked_image(frame_RGB, mask_info['segmentation'])
                pil_img = Image.fromarray(masked_image.astype(np.uint8))
                temp_path = f"/tmp/segment_{os.getpid()}_{segment_id}_{int(time.time()*1000000)}.png"
                pil_img.save(temp_path)
                
                # Generate caption
                prompt = """This image is of an object from a road driving scene (what you see while driving).
                    Describe this object briefly:
                    1. Object type/category (e.g., car, pedestrian, road, traffic sign, tree, building etc)
                    2. Key visual features (color, orientation, condition)
                    
                    Be concise - one or two sentence max. Ignore the black background. Focus on what this object would be in a driving scene."""
                                
                response = ollama.chat(
                    model=self.model_name,
                    messages=[{
                        'role': 'user',
                        'content': prompt,
                        'images': [temp_path]
                    }]
                )
                
                content = response['message']['content'].strip()
