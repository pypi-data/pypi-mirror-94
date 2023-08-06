'''
Contains methods used to resolve a NLU reference to a NLU component.
Handler for getting default components, etcc.
'''


# <<<Name parse procedure>>>
#1.  parse NAMLE data and RETURN IT -> Detect if OC or Closed source (CS)
#2. based on wether OC or CS, use according component resolver
# 2.1 if CS_annotator, then verify licsence/ authenticate, if not do the usual (Make sure all CS imports are in seperate files)
#3. Put all components in NLU pipe and return it
#


# <<<Pythonify procedure>>>
# 1, transform DF
# 2.  Integrate outoputlevel of new annotators by getting some attriubte/str name from them.
# We cannot do isInstance() because we cannot import classes for the cmparioson
# Thus, for OUtput_level inference of singular components and the entiure pipe
# we must first check OC compoments vanilla style and if that fails we must do special infer_CS_component_level() all
# This call must infer the output level without type checks, i.e. use component infos or some string map or some trick (( !! component info!!!)


# 2. Squeeze in 9 Annotators in old extraction process, most annotators are like old ones
#





# 1.AssertionLogReg // CHUNK level // SAME LEVEL AS NER !
# 2.AssertionDL // CHUNK level // SAME LEVEL AS NER !
# 3.Chunk2Token // Helper for Pipe logic most likey internal usage..
# 4.ChunkEntityResolver
# 5.SentenceEntityResolver
# 6.DocumentLogRegClassifier // Skip for now, only trainable. but basically jsut another classifier and nobody would use it since classifier DL coola, right!?
# 7.DeIdentificator // Token LVL, 1 to 1 Map  // Just changes representation of tokens.
    # Actually SUB token, since "Dr Steward Johnson" can become "[DOCTOR]", thus recducing token count
# 8.Contextual Parser// Skip for now, only trainable and file dependent
# 9.RelationExtraction