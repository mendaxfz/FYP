from comparator import positive_comparator,negative_comparator
import time


if __name__ == "__main__":

	value = input("Enter Temperature : ") 
	start_time = time.time()
	print("Output from positive comparator:")
	print(positive_comparator(int(value),clone_to_pcm=False,tref=3))
	print("Output from negative comparator:")
	print(negative_comparator(int(value),clone_to_pcm=False,tref=3))
	print("--- %s seconds ---" % (time.time() - start_time))