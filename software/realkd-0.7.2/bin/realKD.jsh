/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2014-17 The Contributors of the realKD Project
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */
import java.nio.file.FileSystem

import de.unibonn.realkd.algorithms.emm.ExceptionalSubgroupBestFirstBranchAndBound
import de.unibonn.realkd.algorithms.emm.ExceptionalSubgroupSampler
import de.unibonn.realkd.common.workspace.Entity
import de.unibonn.realkd.common.workspace.Workspace
import de.unibonn.realkd.data.table.DataTable
import de.unibonn.realkd.data.propositions.PropositionalContext
import de.unibonn.realkd.patterns.emm.ExceptionalModelPattern
import de.unibonn.realkd.patterns.subgroups.Subgroup

import static de.unibonn.realkd.common.workspace.Workspaces.workspace
import static de.unibonn.realkd.data.propositions.Propositions.propositionalContext
import static de.unibonn.realkd.data.table.XarfImport.xarfImport

FileSystem _fs=java.nio.file.FileSystems.getDefault()
Workspace _ws=workspace(_fs.getPath("."))

void load(Entity... entities) {
	for (Entity entity: entities) {
		_ws.add(entity);
	}
}

ExceptionalSubgroupBestFirstBranchAndBound optimalExceptionalSubgroupDiscovery() {
	return (ExceptionalSubgroupBestFirstBranchAndBound) de.unibonn.realkd.algorithms.AlgorithmFactory.EXCEPTIONAL_SUBGROUP_BESTFIRST_BRANCHANDBOUND.create(_ws);
}

ExceptionalSubgroupSampler randomizedExceptionalSubgroupDiscovery() {
	return (ExceptionalSubgroupSampler) de.unibonn.realkd.algorithms.AlgorithmFactory.EMM_SAMPLER.create(_ws);
}
