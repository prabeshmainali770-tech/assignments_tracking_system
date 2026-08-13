"""
views.py — the "brain" of the assignments app.
"""

from django.shortcuts import redirect, render

from rest_framework import status, viewsets
from rest_framework.response import Response

from .forms import AssignmentForm
from .models import Assignment
from .serializers import AssignmentSerializer


def assignment_list(request):
    """
    Show the "add assignment" form AND the list of assignments on ONE page.
    """

    if request.method == "POST":
        form = AssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("assignments:assignment_list")

    else:
        form = AssignmentForm()

    assignments = Assignment.objects.all()

    return render(
        request,
        "assignments/assignment_list.html",
        {
            "form": form,
            "assignments": assignments,
        },
    )


# ---------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------

class AssignmentViewSet(viewsets.GenericViewSet):
    """
    Complete CRUD API for assignments.
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_object(self):
        """
        Get an assignment using the primary key from the URL.
        """
        pk = self.kwargs.get("pk")
        return Assignment.objects.get(pk=pk)

    # GET /api/assignments/
    def list(self, request):
        """Return every assignment."""
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)

        return Response(serializer.data)

    # POST /api/assignments/
    def create(self, request):
        """Create a new assignment."""
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # PUT /api/assignments/{id}/
    # PATCH /api/assignments/{id}/
    def update(self, request, pk=None):
        """Update an existing assignment."""

        assignment = self.get_object()

        partial = request.method == "PATCH"

        serializer = AssignmentSerializer(
            assignment,
            data=request.data,
            partial=partial,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE /api/assignments/{id}/
    def destroy(self, request, pk=None):
        """Delete an assignment."""

        assignment = self.get_object()
        assignment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )