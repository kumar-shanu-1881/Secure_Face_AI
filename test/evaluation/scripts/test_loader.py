from dataset_loader import loader

print("=" * 60)

lfw = loader.load_lfw()
wider = loader.load_wider()

print("LFW Images :", len(lfw))
print("WIDER Images :", len(wider))

print("\nFirst LFW Sample")

print(lfw[0])

print("\nFirst WIDER Image")

print(wider[0])

print("=" * 60)