This package is a part of [Momotor](https://momotor.org/), a tool for automated processing of digital content. 

Momotor accepts digital content as a product bundle and generates a result bundle from this product under 
control of a recipe bundle. 

Momotor is like a continuous integration system, but broader in scope. The 
type of content that Momotor can process is not restricted; each recipe may impose its own constraints. 
One application of Momotor in an educational setting is the automatic generation of feedback on work submitted 
for programming assignments.

---

The `momotor-bundles` package contains the interfaces to read and write Momotor bundles.

A Momotor bundle is an XML document with optional attachments. Bundles without attachments can be pure XML
documents, bundles with attachments are contained in zip files.

Bundles are at the heart of a Momotor transformation, as a Momotor transformation
takes a recipe, config and product bundle as input and produces a result bundle
as output.

The recipe bundle describes the transformations that need to be performed, the config
bundle provides additional files and configuration to the recipe,
while the product bundle defines the job specific files and configuration.

In an educational setting, the recipe defines a generic way to process a student's
submission, while the config defines the assignment specific details like the
expected answers. The product contains the student's submission.
