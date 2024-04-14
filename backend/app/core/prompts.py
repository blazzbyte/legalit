class Prompts:
    _promptKeywords = """
    # USER INSTRUCTION
    {instruction}
    # LEGAL DOCUMENT
    {document}
    Considering the user's instruction and the content of the legal document to be reviewed, it generates a list of terms or keywords to perform a search in a repository of applicable regulations and laws. These terms should be descriptive, not too short to create ambiguity, nor too long to reduce the efficiency of the search.
    """

    _promptAnalyst = """
    # LEGAL CONTEXT
    {context}
    # USER INSTRUCTION
    {instruction}
    # LEGAL DOCUMENT
    {document}
    Considering the legal context extracted according to a regulatory review, and the user's instruction. Analyze each clause and provision of the legal document, looking for possible areas of compliance or non-compliance. Provide a detailed report summarizing your findings, including any discrepancies or potential risks of non-compliance. Ensure the assessment is thorough and accurate, providing clear recommendations and corrective actions if necessary.
    """

    @staticmethod
    def formatPromptKeywords(instruction: str, document: str) -> str:
        return Prompts._promptKeywords.format(instruction=instruction, document=document)

    @staticmethod
    def formatPromptAnalyst(instruction: str, context: str, document: str) -> str:
        return Prompts._promptAnalyst.format(context=context, instruction=instruction, document=document)