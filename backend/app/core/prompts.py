class Prompts:

    _keywords = """
    # USER INSTRUCTION
    {instruction}
    Considering the user's instruction and the content of the legal document to be reviewed, it generates a list of terms or keywords to perform a search in a repository of applicable regulations and laws. These terms should be descriptive, not too short to create ambiguity, nor too long to reduce the efficiency of the search.
    """

    _keywords_with_document = """
    # USER INSTRUCTION
    {instruction}
    # LEGAL DOCUMENT
    {document}
    Considering the user's instruction and the content of the legal document to be reviewed, it generates a list of terms or keywords to perform a search in a repository of applicable regulations and laws. These terms should be descriptive, not too short to create ambiguity, nor too long to reduce the efficiency of the search.
    """

    _analyst = """
    # LEGAL CONTEXT
    {context}
    Considering the legal context. Respond the user question as better as you can:
    # USER QUESTION
    {instruction}
    """

    _analyst_with_document = """
    # LEGAL CONTEXT
    {context}
    # USER INSTRUCTION
    {instruction}
    # LEGAL DOCUMENT
    {document}
    Considering the legal context extracted according to a regulatory review, and the user's instruction. Analyze each clause and provision of the legal document, looking for possible areas of compliance or non-compliance. Provide a detailed report summarizing your findings, including any discrepancies or potential risks of non-compliance. Ensure the assessment is thorough and accurate, providing clear recommendations and corrective actions if necessary.
    """

    @staticmethod
    def formatPromptKeywords(instruction: str, document: str = "") -> str:
        if document:
            return Prompts._keywords_with_document.format(instruction=instruction, document=document)
        else:
            return Prompts._keywords.format(instruction=instruction)

    @staticmethod
    def formatPromptAnalyst(instruction: str, context: str = "", document: str = "") -> str:
        if document:
            return Prompts._analyst_with_document.format(context=context, instruction=instruction, document=document)
        else:
            return Prompts._analyst.format(context=context, instruction=instruction)